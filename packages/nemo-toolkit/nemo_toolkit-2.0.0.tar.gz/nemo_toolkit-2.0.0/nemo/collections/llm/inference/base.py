# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from pathlib import Path
from typing import Optional, Union

import pytorch_lightning as pl
import torch
import torch.distributed
from megatron.core.inference.common_inference_params import CommonInferenceParams
from megatron.core.inference.engines.mcore_engine import MCoreEngine
from megatron.core.inference.model_inference_wrappers.gpt.gpt_inference_wrapper import GPTInferenceWrapper
from megatron.core.inference.model_inference_wrappers.inference_wrapper_config import InferenceWrapperConfig
from megatron.core.inference.text_generation_controllers.simple_text_generation_controller import (
    SimpleTextGenerationController,
)
from megatron.core.models.gpt.gpt_model import GPTModel as MCoreGPTModel
from pytorch_lightning.trainer.states import TrainerFn

import nemo.lightning as nl
from nemo.collections.llm.peft import LoRA
from nemo.lightning import io
from nemo.lightning.ckpt_utils import ADAPTER_META_FILENAME, ckpt_to_context_subdir, ckpt_to_weights_subdir
from nemo.lightning.pytorch.strategies.megatron_strategy import MegatronStrategy
from nemo.lightning.pytorch.strategies.utils import RestoreConfig


# We need this wrapper since mcore generate uses tokenizer.detokenize, tokenizer.tokenize to encode and decode prompts
class MCoreTokenizerWrappper:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.eod = tokenizer.eod
        self.vocab_size = tokenizer.vocab_size

    def detokenize(self, tokens):
        return self.tokenizer.ids_to_text(tokens)

    def tokenize(self, prompt):
        return self.tokenizer.text_to_ids(prompt)


# TODO: Move to lightning Fabric API.
def _setup_trainer_and_restore_model(path: Path, trainer: nl.Trainer, model: pl.LightningModule):
    assert isinstance(trainer.strategy, MegatronStrategy), "Only MegatronStrategy is supported for trainer.strategy."
    assert trainer.strategy.context_parallel_size <= 1, "Context parallelism is not supported for inference."
    if (adapter_meta_path := ckpt_to_weights_subdir(path) / ADAPTER_META_FILENAME).exists():
        with open(adapter_meta_path, "r") as f:
            metadata = json.load(f)
        restore_config = RestoreConfig(
            path=metadata['model_ckpt_path'],
            load_model_state=True,
            load_optim_state=False,
        )
    else:
        restore_config = RestoreConfig(
            path=path,
            load_model_state=True,
            load_optim_state=False,
        )

    trainer.strategy.restore_config = restore_config
    trainer.strategy._setup_optimizers = False
    trainer.ckpt_path = None
    trainer.strategy.connect(model)
    if trainer.strategy.launcher is not None:
        trainer.strategy.launcher.launch(lambda: None, trainer=trainer)
    trainer.strategy.setup_environment()

    if not model.state_dict():
        model.configure_model()

    trainer.state.fn = TrainerFn.TESTING
    trainer.strategy.setup_megatron_parallel(trainer=trainer)
    trainer.strategy.trainer = trainer
    trainer.strategy.selective_restore()

    lora: Union[io.TrainerContext, LoRA] = io.load_context(ckpt_to_context_subdir(path), "model.model_transform")
    if isinstance(lora, LoRA):
        model = lora(model)
        adapter_sharded_state_dict = {k: v for k, v in model.sharded_state_dict().items() if ".adapter." in k}
        adapter_state = trainer.strategy.checkpoint_io.load_checkpoint(
            ckpt_to_weights_subdir(path), sharded_state_dict=adapter_sharded_state_dict
        )
        trainer.strategy.load_model_state_dict(adapter_state, strict=False)


def setup_model_and_tokenizer(
    path: Path,
    trainer: nl.Trainer,
    params_dtype: torch.dtype = torch.bfloat16,
    inference_batch_times_seqlen_threshold: int = 1000,
) -> tuple[MCoreGPTModel, MCoreTokenizerWrappper]:
    model: io.TrainerContext = io.load_context(path=ckpt_to_context_subdir(path), subpath="model")
    _setup_trainer_and_restore_model(path=path, trainer=trainer, model=model)

    # This is to get the MCore model required in GPTInferenceWrapper.
    mcore_model = model
    while mcore_model:
        if type(mcore_model) is MCoreGPTModel:
            break
        mcore_model = getattr(mcore_model, "module", None)
    if mcore_model is None or type(mcore_model) is not MCoreGPTModel:
        raise ValueError("Exact McoreGPTModel instance not found in the model structure.")

    inference_wrapped_model = GPTInferenceWrapper(
        mcore_model,
        InferenceWrapperConfig(
            hidden_size=mcore_model.config.hidden_size,
            params_dtype=params_dtype,
            inference_batch_times_seqlen_threshold=inference_batch_times_seqlen_threshold,
            padded_vocab_size=model.tokenizer.vocab_size,
        ),
    )

    return inference_wrapped_model, MCoreTokenizerWrappper(model.tokenizer)


def generate(
    model: GPTInferenceWrapper,
    tokenizer: MCoreTokenizerWrappper,
    prompts: list[str],
    max_batch_size: int = 4,
    random_seed: Optional[int] = None,
    inference_params: Optional[CommonInferenceParams] = None,
) -> dict:
    text_generation_controller = SimpleTextGenerationController(inference_wrapped_model=model, tokenizer=tokenizer)
    mcore_engine = MCoreEngine(
        text_generation_controller=text_generation_controller, max_batch_size=max_batch_size, random_seed=random_seed
    )

    common_inference_params = inference_params or CommonInferenceParams(num_tokens_to_generate=512)

    results = mcore_engine.generate(
        prompts=prompts,
        common_inference_params=common_inference_params,
    )

    return results
