from __future__ import annotations

import logging
from dataclasses import replace
from typing import Any, Callable, Iterator, Literal, cast, overload

import numpy as np
from more_itertools import chunked
from pandas import DataFrame

from .embedding_models import EmbeddingModel
from .memory_types import (
    DatasetLike,
    InputType,
    LabeledMemory,
    LabeledMemoryLookup,
    LabeledMemoryLookupColumnResult,
    LookupReturnType,
)
from .storage import LanceDBStorageBackend, MilvusStorageBackend, StorageBackend
from .util import transform_data_to_dict_list

logging.basicConfig(level=logging.INFO)


class LabeledMemorysetV2:
    storage_backend: StorageBackend
    embedding_model: EmbeddingModel

    def __init__(self, uri_or_storage_backend: str | StorageBackend, embedding_model: EmbeddingModel | None = None):
        """
        Initialize a labeled memoryset

        Args:
            uri_or_storage_backend: location of the database for storing the memories. Can be either a
                file or remote URI (e.g. "file:./temp/lance.db#my-memoryset"), or a storage backend object.
            embedding_model: Embedding model to use for semantic similarity search. When reconnecting
                to an existing memoryset the correct embedding model will automatically be loaded, otherwise
                an embedding model must be specified.
        """
        if isinstance(uri_or_storage_backend, str):
            if "milvus" in uri_or_storage_backend:
                logging.info(f"Inferring Milvus storage backend from URI: {uri_or_storage_backend}")
                self.storage_backend = MilvusStorageBackend(uri_or_storage_backend, embedding_model)
            else:
                logging.info(f"Inferring LanceDB storage backend from URI: {uri_or_storage_backend}")
                self.storage_backend = LanceDBStorageBackend(uri_or_storage_backend, embedding_model)
        elif isinstance(uri_or_storage_backend, StorageBackend):
            self.storage_backend = uri_or_storage_backend
        else:
            raise ValueError("url_or_storage_backend must be either a string or a StorageBackend object")

        self.embedding_model = embedding_model or self.storage_backend.embedding_model

        # TODO: add reranker
        self.reranker = None

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        return self.storage_backend.to_list(limit)

    def to_pandas(self, limit: int | None = None) -> DataFrame:
        return DataFrame(self.to_list(limit))

    def __len__(self) -> int:
        return len(self.storage_backend)

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.storage_backend.__iter__()

    def insert(
        self,
        dataset: DatasetLike,
        *,
        log: bool = True,
        compute_embeddings: bool = True,
        batch_size: int = 32,
        only_if_empty: bool = False,
    ):
        """
        Inserts a dataset into the LabeledMemoryset database.

        For dict-like or list of dict-like datasets, there must be a `label` key and one of the following keys: `text`, `image`, or `value`.
        If there are only two keys and one is `label`, the other will be inferred to be `value`.

        For list-like datasets, the first element of each tuple must be the value and the second must be the label.

        Args:
            dataset: data to insert into the memoryset
            log: whether to show a progressbar and log messages
            compute_embeddings: whether to compute embeddings for the dataset or take them from the dataset
            batch_size: the batch size when creating embeddings from memories
            only_if_empty: whether to skip the insert if the memoryset is not empty
        Examples:
            # Example 1: Inserting a dictionary-like dataset
            >>> dataset = [{
            ...    "text": "text 1",
            ...    "label": 0
            ... }]
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)

            # Example 2: Inserting a list-like dataset
            >>> dataset = [
            ...    ("text 1", 0),
            ...    ("text 2", 1)
            ]
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)

            # Example 3: Inserting a Hugging Face Dataset
            from datasets import Dataset
            >>> dataset = load_dataset("frgfm/imagenette", "320px")
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)
        """
        if len(self) and only_if_empty:
            logging.warning("Skipping insert: `only_if_empty` is True and memoryset is not empty.") if log else None
            return
        transformed_data = transform_data_to_dict_list(dataset)
        if len(transformed_data) > 0 and "text" in transformed_data[0]:
            # This sorts the data by text length so that batches are created from similar length samples
            # This smaller amount of added padding decreases overall computational complexity.
            transformed_data = sorted(transformed_data, key=lambda x: -len(x["text"]) if x["text"] is not None else 0)

        if self.embedding_model.transductive_context_length:
            # if the dataset changes by more than 20% and at least 10 items then update the transductive context
            current_size = len(self)
            if len(transformed_data) > 10 and len(transformed_data) > current_size / 5:
                self.embedding_model.update_transductive_context(
                    [m["text"] for m in transformed_data if m["text"] is not None]
                    + (
                        [m.value for m in self.to_list() if m.value is not None and isinstance(m.value, str)]
                        if current_size > 0
                        else []
                    )
                )

        if compute_embeddings:
            # Add embeddings to the transformed data
            embeddings = self.embedding_model.embed(
                cast(list[InputType], [mem["text"] or mem["image"] for mem in transformed_data]),
                show_progress_bar=log,
                value_kind="document",
                batch_size=batch_size,
            )
            for item, embedding in zip(transformed_data, embeddings):
                item["embedding"] = embedding.tolist()
        else:
            if not all(item["embedding"] is not None for item in transformed_data):
                raise ValueError("Embedding must be provided if compute_embeddings is False.")

        for chunk in chunked(transformed_data, batch_size):
            self.storage_backend.insert(list(chunk))

    @overload
    def lookup(
        self,
        query: list[InputType] | np.ndarray,
        *,
        return_type: Literal[LookupReturnType.ROWS, "rows"] = LookupReturnType.ROWS,
        num_memories: int = 1,
        rerank: bool | None = None,
    ) -> list[list[LabeledMemoryLookup]]:
        pass

    @overload
    def lookup(
        self,
        query: InputType,
        *,
        return_type: Literal[LookupReturnType.ROWS, "rows"] = LookupReturnType.ROWS,
        num_memories: int = 1,
        rerank: bool | None = None,
    ) -> list[LabeledMemoryLookup]:
        pass

    @overload
    def lookup(
        self,
        query: list[InputType],
        *,
        return_type: Literal["columns", LookupReturnType.COLUMNS],
        num_memories: int = 1,
        rerank: bool | None = None,
    ) -> LabeledMemoryLookupColumnResult:
        pass

    def lookup(
        self,
        query: InputType | list[InputType] | np.ndarray,
        *,
        return_type: LookupReturnType | str = LookupReturnType.ROWS,
        num_memories: int = 1,
        rerank: bool | None = None,
    ) -> list[list[LabeledMemoryLookup]] | list[LabeledMemoryLookup] | LabeledMemoryLookupColumnResult:
        """
        Retrieves the most similar memories to the query from the memoryset.

        Args:
            query: The query to retrieve memories for. Can be a single value, a list of values, or a numpy array with value embeddings.
            num_memories: The number of memories to retrieve.
            rerank: Whether to rerank the results. If None (default), results will be reranked if a reranker is attached to the Memoryset.

        Returns:
            A list of lists of LabeledMemoryLookups, where each inner list contains the k most similar memories to the corresponding query or a dictionary of columns if the return type is specified as columns.

        Examples:
            # Example 1: Retrieving the most similar memory to a single example
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> query = "Apple"
            >>> memories = memoryset.lookup(query, num_memories=1)
            [
                LabeledMemoryLookup(
                    value='Orange',
                    memory_id=12,
                    memory_version=1,
                    label=0,
                    label_name='fruit',
                    embedding=array([...], dtype=float32),
                    metadata=None,
                    lookup_score=.98,
                    reranker_score=None,
                    reranker_embedding=None
                )
            ]
        """
        # create embedded query matrix of shape num_queries x embedding_dim
        if isinstance(query, np.ndarray):
            embedded_query = query
        elif isinstance(query, list):
            embedded_query = self.embedding_model.embed(query)
        else:
            embedded_query = self.embedding_model.embed([query])

        assert len(embedded_query.shape) == 2, "Query embedding is not in a valid shape"
        assert embedded_query.shape[1] == self.embedding_model.embedding_dim

        # Default reranking to `True` if a reranker is attached and to `False` otherwise.
        rerank = rerank or (rerank is None and self.reranker is not None)
        if rerank:
            if not self.reranker:
                raise ValueError("rerank is set to true but no reranker model has been set on this memoryset")
            num_memories = num_memories * self.reranker.compression

        memories_batch = self.storage_backend.lookup(embedded_query, k=num_memories)

        # rerank the results if necessary
        if rerank:
            assert self.reranker is not None
            if isinstance(query, str):
                queries_list = [query]
            else:
                if not isinstance(query, list) or not isinstance(query[0], str):
                    raise ValueError("reranking only works when passing a string as the query")
                queries_list = cast(list[str], query)
            # TODO: use cached reranker embeddings if available
            reranked_results = [
                self.reranker.rerank(q, memories=[cast(str, m.value) for m in ms], top_k=num_memories)
                for q, ms in zip(queries_list, memories_batch)
            ]
            memories_batch = [
                [
                    LabeledMemoryLookup(
                        reranker_score=reranked_results[j].scores[idx],
                        # TODO: add reranker embedding
                        **memories_batch[j][idx].__dict__,
                    )
                    for idx in reranked_results[j].indices
                ]
                for j in range(len(reranked_results))
            ]

        # return correctly formatted results
        if return_type == "columns":
            return LabeledMemoryLookupColumnResult(
                input_embeddings=[e for e in embedded_query],
                memories_values=[[m.value for m in memories] for memories in memories_batch],
                memories_labels=[[m.label for m in memories] for memories in memories_batch],
                memories_embeddings=[[m.embedding for m in memories] for memories in memories_batch],
                memories_ids=[[m.memory_id for m in memories] for memories in memories_batch],
                memories_versions=[[m.memory_version for m in memories] for memories in memories_batch],
                memories_metadata=[[m.metadata for m in memories] for memories in memories_batch],
                memories_lookup_scores=[[m.lookup_score for m in memories] for memories in memories_batch],
                memories_reranker_scores=[[m.reranker_score for m in memories] for memories in memories_batch],
            )

        if not isinstance(query, list) and not isinstance(query, np.ndarray):
            assert len(memories_batch) == 1
            return memories_batch[0]

        return memories_batch

    def _prepare_destination(
        self, destination_uri_or_memoryset: LabeledMemorysetV2 | str, embedding_model: EmbeddingModel
    ) -> LabeledMemorysetV2:
        if isinstance(destination_uri_or_memoryset, str):
            destination = LabeledMemorysetV2(destination_uri_or_memoryset, embedding_model=embedding_model)
        elif isinstance(destination_uri_or_memoryset, LabeledMemorysetV2):
            destination = destination_uri_or_memoryset

        if destination.storage_backend.uri_with_table_name == self.storage_backend.uri_with_table_name:
            raise ValueError("Destination memoryset cannot be the same as the source memoryset.")

        if len(destination) > 0:
            raise ValueError("Destination memoryset must empty.")

        if (
            embedding_model.name != destination.embedding_model.name
            or embedding_model.version != destination.embedding_model.version
        ):
            raise ValueError(
                f"Destination memoryset has unexpected embedding model. Expected: {embedding_model.name}, Actual: {destination.embedding_model.name}."
            )

        return destination

    def filter(
        self,
        fn: Callable[[LabeledMemory], bool],
        destination_uri_or_memoryset: LabeledMemorysetV2 | str,
    ) -> LabeledMemorysetV2:
        destination = self._prepare_destination(destination_uri_or_memoryset, self.embedding_model)

        values_to_insert = [m for m in self if fn(m)]

        destination.insert(values_to_insert, compute_embeddings=False)

        return destination

    def map(
        self,
        fn: Callable[[LabeledMemory], dict[str, Any]],
        destination_uri_or_memoryset: LabeledMemorysetV2 | str,
    ) -> LabeledMemorysetV2:
        # TODO: This function calculates embeddings one at a time. It should be optimized to calculate embeddings in batches.

        def replace_fn(memory: LabeledMemory) -> LabeledMemory:
            fn_result = fn(memory)

            if not isinstance(fn_result, dict):
                raise ValueError("Map function must return a dictionary with updates.")

            if "embedding" in fn_result:
                raise ValueError(
                    "Embedding cannot be updated. Memoryset automatically calculates embeddings as needed."
                )

            value_changed = "value" in fn_result and memory.value != fn_result["value"]

            if value_changed:
                fn_result["embedding"] = destination.embedding_model.embed(fn_result["value"]).reshape(-1)

            return replace(memory, **fn_result)

        destination = self._prepare_destination(destination_uri_or_memoryset, self.embedding_model)
        mapped_memories = [replace_fn(memory) for memory in self.to_list()]
        destination.insert(mapped_memories, compute_embeddings=False)
        return destination

    def clone(self, uri_or_memoryset: LabeledMemorysetV2 | str) -> LabeledMemorysetV2:
        destination = self._prepare_destination(uri_or_memoryset, self.embedding_model)
        destination.insert(self.to_list(), compute_embeddings=False)
        return destination

    def update_embedding_model(
        self,
        embedding_model: EmbeddingModel,
        destination_uri_or_memoryset: LabeledMemorysetV2 | str,
    ) -> LabeledMemorysetV2:
        destination = self._prepare_destination(destination_uri_or_memoryset, embedding_model)
        destination.insert(self.to_list(), compute_embeddings=True)
        return destination
