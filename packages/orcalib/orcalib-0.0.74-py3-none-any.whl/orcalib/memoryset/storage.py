from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterator

import numpy as np

from .memory_types import LabeledMemory, LabeledMemoryLookup
from .util import MemoryToInsert

logging.basicConfig(level=logging.INFO)

# 2 weeks in seconds
CACHE_TTL = 1.21e6


@dataclass(frozen=True)
class MemorysetMetadata:
    embedding_dim: int
    embedding_model_name: str
    embedding_model_version: int
    embedding_model_query_prompt: str | None
    embedding_model_document_prompt: str | None
    embedding_model_max_seq_length: int | None


class StorageBackend(ABC):
    table_name: str
    database_uri: str
    is_local_database: bool
    connected: bool = False

    def __init__(
        self,
        table_name: str,
        database_uri: str,
    ) -> None:
        """
        Create a storage backend for the memoryset without connecting to it.

        Warning:
            Before performing any operations on the storage backend other than `drop` and
            `get_metadata`, you must call `connect` on it.

        Args:
            table_name: Name of the table to use for the memoryset
            database_uri: URI of the database to connect to
        """
        self.table_name = table_name
        self.database_uri = database_uri

    @abstractmethod
    def drop(self):
        """
        Drop the data table of the memoryset and delete its metadata.

        Notes:
            This does not drop the database file itself, only the data table for the memoryset and
            the row for the memoryset's metadata. If the memoryset has not been created yet, this
            operation is a no-op.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> MemorysetMetadata | None:
        """
        Get the metadata for the memoryset if it exists.

        Notes:
            This will not create a local database file if it does not exist.

        Returns:
            Metadata for the memoryset or None if the memoryset has not been created yet.
        """
        pass

    @abstractmethod
    def connect(self, metadata: MemorysetMetadata) -> StorageBackend:
        """
        Connect to the database, initialize the database and memories table if necessary, and upsert
        the metadata for the memoryset.
        """
        pass

    def reset(self, metadata: MemorysetMetadata):
        """
        Drop the table of the memoryset and delete its metadata, then recreate it.
        """
        self.drop()
        self.connect(metadata)

    @abstractmethod
    def insert(self, data: list[MemoryToInsert]) -> None:
        pass

    @abstractmethod
    def lookup(self, query: np.ndarray, k: int) -> list[list[LabeledMemoryLookup]]:
        pass

    @abstractmethod
    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[LabeledMemory]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, StorageBackend):
            return False
        return self.database_uri == other.database_uri and self.table_name == other.table_name
