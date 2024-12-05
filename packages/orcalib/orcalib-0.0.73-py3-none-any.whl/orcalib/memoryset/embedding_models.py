from __future__ import annotations

import logging
import os
import random
from dataclasses import dataclass
from typing import Literal, cast

import numpy as np
from sentence_transformers import SentenceTransformer
from torch import Tensor
from tqdm.auto import trange
from transformers import AutoConfig, CLIPConfig, PretrainedConfig

from ..torch_layers import SentenceEmbeddingGenerator
from .memory_types import InputType


@dataclass
class EmbeddingModelConfig:
    """
    Configuration for an embedding model

    Note:
        Apart from the model name, this contains properties that are not correctly specified in the
        AutoConfig object that is saved with the model for some reason and thus needs to be
        overwritten at initialization to ensure correct behavior.
    """

    name: str
    """
    Either the name of a HuggingFace model or a path to a local saved model,

    Note:
        Only models that are available as class properties like `EmbeddingModel.CLIP_BASE` as well
        as fine-tuned versions of them are guaranteed to work
    """

    # TODO: consider removing this, HuggingFace supports a revision number that we could use instead
    version: int = 0
    """Optional version number, used for default models to distinguish changes in models with the same name"""

    embedding_dim: int | None = None
    """Optional overwrite for embeddings dimension in case it is not correctly saved on HuggingFace"""

    query_prompt: str | None = None
    """Optional prompt prefix to use for queries with this model"""

    document_prompt: str | None = None
    """Optional prompt prefix to use for documents with this model"""


class EmbeddingModelMeta(type):
    _default_models: dict[str, EmbeddingModel] = {}

    @property
    def CLIP_BASE(cls) -> EmbeddingModel:
        """[CLIP-L14](https://huggingface.co/sentence-transformers/clip-ViT-L-14) embedding model"""
        if "clip_base" not in cls._default_models:
            cls._default_models["clip_base"] = EmbeddingModel(
                EmbeddingModelConfig(
                    name="sentence-transformers/clip-ViT-L-14",
                    version=1,
                    embedding_dim=768,  # wrongly specified as 512 in the AutoConfig
                )
            )
        return cls._default_models["clip_base"]

    @property
    def GTE_BASE(cls) -> EmbeddingModel:
        """[Alibaba GTE-Base v1.5](https://huggingface.co/Alibaba-NLP/gte-base-en-v1.5) embedding model"""
        if "gte_base" not in cls._default_models:
            cls._default_models["gte_base"] = EmbeddingModel(
                EmbeddingModelConfig(name="Alibaba-NLP/gte-base-en-v1.5", version=1)
            )
        return cls._default_models["gte_base"]

    @property
    def CDE_SMALL(cls) -> EmbeddingModel:
        """[CDE-Small](https://huggingface.co/jxm/cde-small-v1) embedding model"""
        if "cde_small" not in cls._default_models:
            cls._default_models["cde_small"] = EmbeddingModel(
                EmbeddingModelConfig(
                    name="jxm/cde-small-v1",
                    version=1,
                    embedding_dim=768,  # not specified in the AutoConfig
                    query_prompt="search_query: ",
                    document_prompt="search_document: ",
                )
            )
        return cls._default_models["cde_small"]


class EmbeddingModel(metaclass=EmbeddingModelMeta):
    """
    Embedding models for use with memorysets
    """

    model_whitelist = [
        "sentence-transformers/clip-ViT-L-14",
        "Alibaba-NLP/gte-base-en-v1.5",
        "Alibaba-NLP/gte-large-en-v1.5",
        "sentence-transformers/multi-qa-mpnet-base-dot-v1",
        "distilbert-base-uncased",
        "distilbert-base-cased",
        "bert-base-cased",
        "bert-base-uncased",
        "roberta-base",
        "roberta-large",
        "jxm/cde-small-v1",
        "microsoft/mpnet-base",
    ]

    def __init__(
        self,
        config: EmbeddingModelConfig,
    ):
        """
        Initialize an embedding model

        Warning:
            Only the models that are available as class properties like `EmbeddingModel.CLIP_BASE` as
            well as fine-tuned versions of them are guaranteed to work.

        Args:
            config: configuration for the embedding model
        """
        self.config = config
        if config.name not in self.model_whitelist and not os.path.isdir(config.name):
            logging.warning(f"Model {config.name} is not in the whitelist, it may not work correctly")
        self.name = config.name
        self.version = config.version
        model_config: PretrainedConfig = AutoConfig.from_pretrained(self.name, trust_remote_code=True)
        if config.embedding_dim is not None:
            self.embedding_dim = config.embedding_dim
        else:
            self.embedding_dim = cast(
                int, getattr(model_config, "projection_dim", getattr(model_config, "hidden_size", None))
            )
            if self.embedding_dim is None:
                raise ValueError(f"Could not determine embedding dimension from {model_config}")
        self.query_prompt = config.query_prompt
        self.document_prompt = config.document_prompt
        self.transductive_context_length: int | None = getattr(model_config, "transductive_corpus_size", None)
        self.transductive_context: None | Tensor = None
        self._max_sequence_length: int | None = getattr(model_config, "max_seq_length", None)
        self._use_sentence_transformer: bool = (
            isinstance(model_config, CLIPConfig) or type(model_config).__name__ == "ContextualModelConfig"
        )

    def __repr__(self) -> str:
        return f"EmbeddingModel({self.name}, version={self.version}, embedding_dim={self.embedding_dim})"

    @property
    def embedder(self) -> SentenceTransformer | SentenceEmbeddingGenerator:
        if not hasattr(self, "_embedder"):
            if self._use_sentence_transformer:
                self._embedder = SentenceTransformer(self.name, trust_remote_code=True)
            else:
                self._embedder = SentenceEmbeddingGenerator(base_model=self.name, frozen=True, normalize=True)
        return self._embedder

    @property
    def max_sequence_length(self) -> int:
        if self._max_sequence_length is not None:
            return self._max_sequence_length
        if isinstance(self.embedder, SentenceTransformer):
            return self.embedder.max_seq_length
        else:
            return self.embedder.max_sequence_length

    @max_sequence_length.setter
    def max_sequence_length(self, value: int):
        if isinstance(self.embedder, SentenceTransformer):
            self.embedder.max_seq_length = value
        else:
            self.embedder.max_sequence_length = value
        self._max_sequence_length = value

    def update_transductive_context(self, values: list[str]) -> None:
        """
        Update the context used by contextual embedding models like [CDE](https://huggingface.co/jxm/cde-small-v1)

        Args:
            values: the values of the corpus to construct the context from
        """
        if self.transductive_context_length is not None and isinstance(self.embedder, SentenceTransformer):
            logging.info("Updating transductive context for embedding model")
            self.transductive_context = self.embedder.encode(
                random.sample(values, k=self.transductive_context_length),
                prompt=self.document_prompt,
                convert_to_tensor=True,
                show_progress_bar=False,
            )

    def embed(
        self,
        values: InputType | list[InputType],
        show_progress_bar: bool = False,
        batch_size: int = 32,
        value_kind: Literal["query", "document"] = "query",
    ) -> np.ndarray:
        """
        Generate embeddings for the given input

        Args:
            data: the data to encode, will be converted to a list if a scalar is given
            show_progress_bar: whether to show a progress bar
            batch_size: size of the batches to use
            value_kind: kind of values to embed, either "query" or "document" to determine potential
                prompts for the model, this is usually just used by memoryset internally
        Returns:
            matrix with embeddings of shape `len_data` x `embedding_dim`
        """
        values = [values] if not isinstance(values, list) else values
        if len(values) == 0:
            return np.empty((0,))
        # generate embeddings
        if isinstance(self.embedder, SentenceTransformer):
            return self.embedder.encode(
                values,  # type: ignore -- types are wrong, image is accepted here
                show_progress_bar=show_progress_bar,
                normalize_embeddings=True,
                batch_size=batch_size,
                prompt=self.document_prompt if value_kind == "document" else self.query_prompt,
                dataset_embeddings=self.transductive_context,
            )
        else:
            if not isinstance(values[0], str):
                raise ValueError(f"{self.name} embedding model only supports strings")
            if len(values) <= batch_size:
                return self.embedder.encode(cast(list[str], values)).cpu().numpy()
            else:
                results = []
                for i in trange(
                    0,
                    len(values),
                    batch_size,
                    disable=not show_progress_bar,
                ):
                    batch = cast(list[str], values[i : i + batch_size])
                    results.append(self.embedder.encode(batch).cpu().numpy())
                return np.vstack(results)
