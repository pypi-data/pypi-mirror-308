# SPDX-FileCopyrightText: Copyright (c) 1993-2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from contextlib import contextmanager
from typing import Dict, Generator

import torch
from torch import nn
from transformers import LlamaForCausalLM, MistralForCausalLM, Phi3ForCausalLM, PreTrainedModel, Qwen2ForCausalLM

logger = logging.getLogger(__name__)


class BasePress:
    """Base class for pruning methods.
    Each pruning method should implement a `score` method that computes the scores for each KV pair in a layer.
    This score is used to prune the KV pairs with the lowest scores in the `hook` method
    The `hook` method is called after the forward pass of a layer and updates the cache with the pruned KV pairs.
    The press can be applied to a model by calling it with the model as an argument.
    """

    def __init__(self, compression_ratio: float = 0.0):
        self.compression_ratio = compression_ratio
        assert 0 <= compression_ratio < 1, "Compression ratio must be between 0 and 1"

    def score(
        self,
        module: nn.Module,
        hidden_states: torch.Tensor,
        keys: torch.Tensor,
        values: torch.Tensor,
        attentions: torch.Tensor,
        kwargs,
    ) -> torch.Tensor:
        """Compute the scores for each KV pair in the layer.

        Parameters
        ----------
        module :
            Transformer layer, see `hook` method for more details.
        hidden_states :
            Hidden states of the layer.
        keys :
            Keys of the cache. Note keys are after RoPE.
        values :
            Values of the cache.
        attentions :
            Attention weights of the layer.
        kwargs :
            Keyword arguments, as given to the forward pass of the layer.

        Returns
        -------
            Scores for each KV pair in the layer, shape keys.shape[:-1].

        """
        raise NotImplementedError

    def forward_hook(self, module: nn.Module, input: list[torch.Tensor], kwargs: Dict, output: list):
        """Cache compression hook called after the forward pass of a decoder layer.
        The hook is applied only during the pre-filling phase if there is some pruning ratio.
        The current implementation only allows to remove a constant number of KV pairs.

        Parameters
        ----------
        module :
            Transformer attention layer.
        input :
            Input to the hook. This is the input to the forward pass of the layer.
        kwargs :
            Keyword arguments, as given to the forward pass of the layer.
        output :
            Output of the hook. This is the original output of the forward pass of the layer.

        Returns
        -------
            Modified output of the forward pass of the layer.

        """
        # See e.g. LlamaDecoderLayer.forward for the output structure
        if len(output) == 3:
            _, attentions, cache = output
        else:
            attentions, cache = None, output[-1]

        hidden_states = kwargs["hidden_states"]
        q_len = hidden_states.shape[1]

        # Don't compress if the compression ratio is 0 or this is not pre-filling
        if (self.compression_ratio == 0) or (cache.seen_tokens > q_len):
            return output

        keys = cache.key_cache[module.layer_idx]
        values = cache.value_cache[module.layer_idx]

        with torch.no_grad():
            scores = self.score(module, hidden_states, keys, values, attentions, kwargs)

        # Prune KV pairs with the lowest scores
        n_kept = int(q_len * (1 - self.compression_ratio))
        indices = scores.topk(n_kept, dim=-1).indices
        indices = indices.unsqueeze(-1).expand(-1, -1, -1, module.head_dim)

        # Update cache
        cache.key_cache[module.layer_idx] = keys.gather(2, indices)
        cache.value_cache[module.layer_idx] = values.gather(2, indices)

        return output

    @contextmanager
    def __call__(self, model: PreTrainedModel) -> Generator:
        """
        Context manager to apply a compression method to a model.
        Apply this context manager during the pre-filling phase to compress the context.

        Parameters
        ----------
        model : PreTrainedModel
            Model to apply the compression method to
        """

        if not isinstance(model, (LlamaForCausalLM, MistralForCausalLM, Phi3ForCausalLM, Qwen2ForCausalLM)):
            logger.warning(f"Model {type(model)} not tested")

        try:
            hooks = []
            for layer in model.model.layers:
                hooks.append(layer.self_attn.register_forward_hook(self.forward_hook, with_kwargs=True))

            yield
        finally:
            for forward_hook in hooks:
                forward_hook.remove()
