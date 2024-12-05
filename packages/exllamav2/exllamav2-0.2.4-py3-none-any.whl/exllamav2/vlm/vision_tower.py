from __future__ import annotations
import os, sys

import threading

import torch
from exllamav2 import ExLlamaV2, ExLlamaV2Tokenizer
from exllamav2.conv2d import ExLlamaV2Conv2D
from exllamav2.rmsnorm import ExLlamaV2RMSNorm
from exllamav2.attn import ExLlamaV2Attention
from exllamav2.mlp import ExLlamaV2MLP
from exllamav2.config import ExLlamaV2Config
from exllamav2.module import ExLlamaV2Module
from exllamav2.vlm.processor import pixtral
from exllamav2.compat import safe_move_tensor
from exllamav2.generator import ExLlamaV2MMEmbedding
from typing import Callable

from PIL.Image import Image
from exllamav2.vlm.util import position_ids_in_meshgrid

class ExLlamaV2VisionTower(ExLlamaV2):

    config: ExLlamaV2Config
    modules: list[ExLlamaV2Module]

    # noinspection PyMissingConstructor
    def __init__(
        self,
        config: ExLlamaV2Config
    ):
        self.config = config
        cfg = self.config
        self.archparams = cfg.arch.vt
        self.modules = []

        # Preprocessor

        if cfg.vision_model_type == "pixtral":
            self.preprocess_func = pixtral.preprocess
            self.postprocess_func = pixtral.postprocess
        else:
            raise ValueError(f"Unknown vision model type: {cfg.vision_model_type}")

        # Position embeddings

        self.p_maxedge = cfg.vision_size["longest_edge"] // cfg.vision_patch_size["width"]
        freqs = 1.0 / (cfg.vision_rope_theta ** (torch.arange(0, cfg.vision_head_dim, 2).float() / cfg.vision_head_dim))
        h = torch.arange(self.p_maxedge, device=freqs.device)
        w = torch.arange(self.p_maxedge, device=freqs.device)
        freqs_h = torch.outer(h, freqs[::2]).float()
        freqs_w = torch.outer(w, freqs[1::2]).float()
        inv_freq = torch.cat(
            [
                freqs_h[:, None, :].repeat(1, self.p_maxedge, 1),
                freqs_w[None, :, :].repeat(self.p_maxedge, 1, 1),
            ],
            dim=-1,
        ).reshape(-1, cfg.vision_head_dim // 2)
        inv_freq = torch.cat((inv_freq, inv_freq), dim = -1)

        self.rope_cos = inv_freq.cos().half()
        self.rope_sin = inv_freq.sin().half()

        # Patch embeddings

        patch_size = tuple(config.vision_patch_size[x] for x in ["height", "width"])
        patch_conv = ExLlamaV2Conv2D(
            model = self,
            key = cfg.arch.vt_prefix + "patch_conv",
            in_channels = self.config.vision_num_channels,
            out_channels = self.config.vision_hidden_size,
            kernel_size = patch_size,
            has_bias = self.archparams.patch_conv_bias,
            archparams = self.archparams,
        )
        self.modules += [patch_conv]

        # Input norm

        norm = ExLlamaV2RMSNorm(
            model = self,
            key = cfg.arch.vt_prefix + "ln_pre",
            archparams = self.archparams,
        )
        self.modules += [norm]

        # Decoder layers

        for layer_idx in range(self.config.vision_num_layers):
            layer_key = cfg.arch.vt_prefix + f"transformer.layers.{layer_idx}"
            attn = ExLlamaV2Attention(self, layer_key, layer_idx, archparams = self.archparams)
            mlp = ExLlamaV2MLP(self, layer_key, layer_idx, archparams = self.archparams)
            self.modules += [attn, mlp]

        # Multimodal projection

        mmp = ExLlamaV2MLP(
            self,
            cfg.arch.mmp_prefix,
            0,
            archparams = cfg.arch.mmp,
            in_features = cfg.vision_hidden_size,
            out_features = cfg.hidden_size,
            interm_features = cfg.hidden_size,
            has_norm = False,
            has_residual = False
        )
        self.modules += [mmp]


    def forward(self, **kwargs):
        raise NotImplementedError()
    def forward_chunk(self, **kwargs):
        raise NotImplementedError()
    def load_tp(self, **kwargs):
        raise ValueError("load_tp not supported for vision model")
    def load_tp_gen(self, **kwargs):
        raise ValueError("load_tp not supported for vision model")
    def load_autosplit(self, **kwargs):
        raise ValueError("load_autosplit not supported for vision model")
    def load_autosplit_gen(self, **kwargs):
        raise ValueError("load_autosplit not supported for vision model")


    def process(
        self,
        hidden_states: torch.Tensor,
        abort_event: threading.Event | None = None,
        **kwargs
    ):
        cfg = self.config

        if len(hidden_states.shape) == 3:
            hidden_states = hidden_states.unsqueeze(0)

        bsz, channels, height, width = hidden_states.shape

        p_height = height // cfg.vision_patch_size["height"]
        p_width = width // cfg.vision_patch_size["width"]
        position_ids = position_ids_in_meshgrid(p_height, p_width, self.p_maxedge)

        cos = self.rope_cos[position_ids]
        sin = self.rope_sin[position_ids]
        attn_params = ExLlamaV2Attention.Params(non_causal_attn = True)

        device = self.modules[0].device_idx
        for idx, module in enumerate(self.modules):

            # Respect abort signal

            if abort_event and abort_event.is_set():
                return None, None

            # Onward

            n_device = module.device_idx
            if idx == 0 or (n_device is not None and n_device != device and n_device >= 0):
                hidden_states = safe_move_tensor(hidden_states, n_device, non_blocking = True)

            if cos.device != hidden_states.device:
                cos = safe_move_tensor(cos, hidden_states.device)
                sin = safe_move_tensor(sin, hidden_states.device)

            hidden_states = module.forward(
                hidden_states,
                attn_params = attn_params,
                **kwargs | {
                    "alt_rope_embedding": (cos, sin)
                }
            )

        return hidden_states


    def get_image_embeddings(
        self,
        model: ExLlamaV2,
        tokenizer: ExLlamaV2Tokenizer,
        image: Image,
        text_alias: str,
    ) -> ExLlamaV2MMEmbedding:
        """
        :param model:
            Text model for which to produce embeddings

        :param tokenizer:
            Tokenizer

        :param image:
            Input PIL image

        :param text_alias:
            Text string to represent this embedding for tokenizing

        :return:
            ExLlamaV2MMEmbedding
        """

        width, height = image.size
        original_size = (height, width)

        image_tensor = self.preprocess_func(self.config, image)
        image_size = tuple(image_tensor.shape[1:])

        embedding_tensor = self.process(image_tensor)

        features_y = image_size[0] // 16
        features_x = image_size[1] // 16

        embedding_tensor = self.postprocess_func(
            model,
            tokenizer,
            embedding_tensor[0],
            features_y,
            features_x,
        )

        mme = ExLlamaV2MMEmbedding(
            model = model,
            embeddings = embedding_tensor,
            text_alias = text_alias
        )

        mme.metadata.update({
            "original_size": original_size,
            "preprocessed_size": image_size,
            "patches_size": (features_y, features_x),
        })

        return mme