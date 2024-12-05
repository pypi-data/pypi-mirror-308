import base64
import json
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Iterator

import lancedb
import numpy as np
import pyarrow as pa
from cachetools import TTLCache
from PIL import Image
from pymilvus import DataType, MilvusClient

from .embedding_models import EmbeddingModel, EmbeddingModelConfig
from .memory_types import LabeledMemory, LabeledMemoryLookup
from .util import (
    MemoryToInsert,
    bytes_to_pil_image,
    get_embedding_hash,
    pil_image_to_bytes,
)

logging.basicConfig(level=logging.INFO)

# 2 weeks in seconds
CACHE_TTL = 1.21e6


class StorageBackendType(Enum):
    LANCE_DB = "lance_db"
    MILVUS = "milvus"


class StorageBackend(ABC):
    DEFAULT_TABLE_NAME = "memories"

    def __init__(self, uri: str, embedding_model: EmbeddingModel | None = None) -> None:
        """
        Initializes the storage backend with the given URI and optional embedding model.

        Args:
            uri (str): The URI of the storage backend. It should be in the format `backend_uri#table_name`, or just `backend_uri` in which case
                the default table name "memories" will be used.
            embedding_model (EmbeddingModel, optional): An optional embedding model. If not provided,
                the embedding model configuration will be loaded from the storage backend.

        Raises:
            ValueError: If the embedding model configuration is not provided and cannot be loaded from the storage backend.
        """
        self.db_uri, self.table_name = self._parse_uri(uri)

        self.connect()
        self.initialize_meta_table()

        if embedding_model is None:
            loaded_embedding_model_config = self.load_embedding_model_config()

            if loaded_embedding_model_config is None:
                raise ValueError("Embedding model configuration must be provided for new memoryset initialization")

            self.embedding_model = EmbeddingModel(loaded_embedding_model_config)
        else:
            loaded_embedding_model_config = self.load_embedding_model_config()

            if loaded_embedding_model_config is not None:
                if (
                    loaded_embedding_model_config.name != embedding_model.config.name
                    or loaded_embedding_model_config.version != embedding_model.config.version
                ):
                    raise ValueError(
                        "Provided embedding model configuration does not match the one stored in the backend"
                    )

            self.embedding_model = embedding_model
            self.write_metadata(self.embedding_model.config)

        self.initialize_data_table(self.embedding_model.embedding_dim)

    @staticmethod
    def _parse_uri(uri: str) -> tuple[str, str]:
        """
        Parses a URI to extract the base URI and table name.

        Args:
            uri (str): The URI string to be parsed. The URI may contain a table name
                       separated by a '#' character.

        Returns:
            tuple[str, str]: A tuple containing the base URI and the table name. If
                             the table name is not specified in the URI, the default
                             table name is returned.
        """
        if "#" in uri:
            uri, table_name = uri.split("#")
            return uri, table_name
        else:
            return uri, StorageBackend.DEFAULT_TABLE_NAME

    @property
    def uri_with_table_name(self) -> str:
        return f"{self.db_uri}#{self.table_name}"

    @property
    def uri_without_table_name(self) -> str:
        return self.db_uri

    @abstractmethod
    def connect(self) -> Any:
        pass

    @abstractmethod
    def initialize_meta_table(self) -> None:
        pass

    @abstractmethod
    def initialize_data_table(self, embedding_model_dim: int) -> None:
        pass

    @abstractmethod
    def write_metadata(self, embedding_model_config: EmbeddingModelConfig) -> None:
        pass

    @abstractmethod
    def load_embedding_model_config(self) -> EmbeddingModelConfig | None:
        pass

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

    @abstractmethod
    def drop_table(self):
        pass


class LanceDBStorageBackend(StorageBackend):
    METADATA_TABLE_NAME = "memoryset_metadata"

    def __init__(self, uri: str, embedding_model: EmbeddingModel | None = None) -> None:
        super().__init__(uri, embedding_model)
        self._cache = TTLCache(maxsize=25000, ttl=CACHE_TTL)

    def connect(self) -> Any:
        self._db = lancedb.connect(self.db_uri)

    def initialize_meta_table(self) -> None:
        if LanceDBStorageBackend.METADATA_TABLE_NAME not in self._db.table_names():
            return self._db.create_table(
                LanceDBStorageBackend.METADATA_TABLE_NAME,
                schema=pa.schema(
                    [
                        pa.field("memoryset_table_name", pa.string()),
                        pa.field("embedding_model_name", pa.string()),
                        pa.field("embedding_model_version", pa.int64()),
                        pa.field("embedding_model_embedding_dim", pa.int64()),
                        pa.field("embedding_model_query_prompt", pa.string()),
                        pa.field("embedding_model_document_prompt", pa.string()),
                    ]
                ),
            )

    def initialize_data_table(self, embedding_model_dim: int) -> None:
        if self.table_name not in self._db.table_names():
            schema = pa.schema(
                [
                    pa.field("text", pa.string()),
                    pa.field("image", pa.binary()),
                    pa.field("label", pa.int64()),
                    pa.field("label_name", pa.string()),
                    pa.field("metadata", pa.string()),
                    pa.field("memory_version", pa.int64()),
                    pa.field(
                        "embedding",
                        pa.list_(pa.float32(), list_size=embedding_model_dim),
                    ),
                ]
            )

            self._db.create_table(self.table_name, schema=schema, exist_ok=False)

    def write_metadata(self, metadata: EmbeddingModelConfig) -> None:
        metadata_table = self._db.open_table(LanceDBStorageBackend.METADATA_TABLE_NAME)
        metadata_table.merge_insert(
            "memoryset_table_name"
        ).when_matched_update_all().when_not_matched_insert_all().execute(
            [
                {
                    "memoryset_table_name": self.table_name,
                    "embedding_model_name": metadata.name,
                    "embedding_model_version": metadata.version,
                    "embedding_model_embedding_dim": metadata.embedding_dim,
                    "embedding_model_query_prompt": metadata.query_prompt,
                    "embedding_model_document_prompt": metadata.document_prompt,
                }
            ]
        )

    def load_embedding_model_config(self) -> EmbeddingModelConfig | None:
        metadata_table = self._db.open_table(LanceDBStorageBackend.METADATA_TABLE_NAME)

        metadata_rows = metadata_table.search().where(f"memoryset_table_name == '{self.table_name}'").to_list()

        if len(metadata_rows) == 0:
            return None

        if len(metadata_rows) > 1:
            raise ValueError("found multiple metadata entries for memoryset")

        metadata = metadata_rows[0]

        return EmbeddingModelConfig(
            name=metadata["embedding_model_name"],
            version=metadata["embedding_model_version"],
            embedding_dim=metadata["embedding_model_embedding_dim"],
            query_prompt=metadata["embedding_model_query_prompt"],
            document_prompt=metadata["embedding_model_document_prompt"],
        )

    def _prepare_for_insert(self, datum: MemoryToInsert) -> dict[str, Any]:
        if datum["image"] is not None:
            image_bytes = pil_image_to_bytes(datum["image"])
        else:
            image_bytes = None

        return {
            "text": datum["text"],
            "image": image_bytes,
            "label": datum["label"],
            "label_name": datum["label_name"],
            "metadata": datum["metadata"],
            "memory_version": datum["memory_version"],
            "embedding": datum["embedding"],
        }

    def insert(self, data: list[MemoryToInsert]) -> None:
        if len(data) == 0:
            return

        data_to_insert = [self._prepare_for_insert(d) for d in data]

        self._db.open_table(self.table_name).add(data_to_insert)

    def lookup(self, query: np.ndarray, k: int) -> list[list[LabeledMemoryLookup]]:
        if len(query.shape) != 2:
            raise ValueError("Query must be a 2D numpy array")

        def single_lookup(q: np.ndarray) -> list[LabeledMemoryLookup]:
            cache_key = (get_embedding_hash(q), k)
            result = self._cache.get(cache_key, None)

            if result is None:
                result = self._db.open_table(self.table_name).search(q).with_row_id(True).limit(k).to_list()
                self._cache[cache_key] = result

            return [self._to_labeled_memory_lookup(row, q) for row in result]

        return [single_lookup(q) for q in query]

    def drop_table(self):
        self._db.drop_table(self.table_name)

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.to_list().__iter__()

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        # TODO: with_row_id does not actually work https://github.com/lancedb/lancedb/issues/1724
        query_results = self._db.open_table(self.table_name).search().with_row_id(True).limit(limit).to_list()

        return [self._to_labeled_memory(row) for row in query_results]

    def __len__(self) -> int:
        return self._db.open_table(self.table_name).count_rows()

    def _to_labeled_memory_lookup(self, row: dict[str, Any], query: np.ndarray) -> LabeledMemoryLookup:
        metadata = json.loads(row["metadata"]) if row["metadata"] is not None else {}
        embedding = np.array(row["embedding"], dtype=np.float32)
        value = bytes_to_pil_image(row["image"]) if row["image"] is not None else row["text"]

        return LabeledMemoryLookup(
            embedding=embedding,
            label_name=row["label_name"],
            label=row["label"],
            lookup_score=float(np.dot(query, embedding)),
            memory_id=row["_rowid"],
            memory_version=row["memory_version"],
            metadata=metadata,
            value=value,
        )

    def _to_labeled_memory(self, row: dict[str, Any]) -> LabeledMemory:
        metadata = json.loads(row["metadata"]) if row["metadata"] is not None else {}
        embedding = np.array(row["embedding"], dtype=np.float32)
        value = bytes_to_pil_image(row["image"]) if row["image"] is not None else row["text"]

        return LabeledMemory(
            embedding=embedding,
            label_name=row.get("label_name", None),
            label=row["label"],
            memory_id=row.get("_rowid", None),
            memory_version=row.get("memory_version", 1),
            metadata=metadata,
            value=value,
        )


class MilvusStorageBackend(StorageBackend):
    METADATA_TABLE_NAME = "memoryset_metadata"

    def __init__(
        self,
        uri,
        embedding_model=None,
        metric_type: str = "IP",
        index_type: str = "FLAT",
        index_params: dict = {},
    ):
        self.metric_type = metric_type
        self.index_type = index_type
        self.index_params = index_params

        super().__init__(uri, embedding_model)

    @staticmethod
    def _none_to_empty(value: Any | None, klass) -> Any:
        if klass == str:
            return value if value is not None else ""
        elif klass == int:
            return value if value is not None else 0
        elif klass == float:
            return value if value is not None else 0.0
        elif klass == dict:
            return value if value is not None else {}
        elif klass == list:
            return value if value is not None else []
        elif klass == bytes:
            return value if value is not None else ""
        else:
            raise ValueError(f"Unsupported class {klass}")

    @staticmethod
    def _empty_to_none(value: Any, klass) -> Any:
        if klass == str:
            return value if value != "" else None
        elif klass == int:
            return value if value != 0 else None
        elif klass == float:
            return value if value != 0.0 else None
        elif klass == dict:
            return value if value != {} else None
        elif klass == list:
            return value if value != [] else None
        else:
            raise ValueError(f"Unsupported class {klass}")

    @staticmethod
    def _encode_image(image: Image.Image) -> str:
        image_bytes = pil_image_to_bytes(image)
        image_str = base64.b64encode(image_bytes).decode("utf-8")
        return image_str

    @staticmethod
    def _decode_image(image_str: str) -> Image.Image:
        image_bytes = base64.b64decode(image_str)
        return bytes_to_pil_image(image_bytes)

    @staticmethod
    def _prepare_for_insert(datum: MemoryToInsert) -> dict[str, Any]:
        if datum["image"] is not None:
            image_str = MilvusStorageBackend._encode_image(datum["image"])
        else:
            image_str = ""

        return {
            "text": MilvusStorageBackend._none_to_empty(datum["text"], str),
            "image": image_str,
            "label": MilvusStorageBackend._none_to_empty(datum["label"], int),
            "label_name": MilvusStorageBackend._none_to_empty(datum["label_name"], str),
            "metadata": datum["metadata"] or "{}",
            "memory_version": MilvusStorageBackend._none_to_empty(datum["memory_version"], int),
            "embedding": MilvusStorageBackend._none_to_empty(datum["embedding"], list),
        }

    def _create_collection(self, embedding_dim: int) -> None:
        schema = self._client.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=embedding_dim, is_primary=False)
        schema.add_field("label", DataType.INT64, is_primary=False)
        schema.add_field("label_name", DataType.VARCHAR, is_primary=False, max_length=256)
        schema.add_field("metadata", DataType.VARCHAR, is_primary=False, max_length=2048)
        schema.add_field("memory_version", DataType.INT64, is_primary=False)
        schema.add_field("text", DataType.VARCHAR, is_primary=False, max_length=2048)
        # schema.add_field("image", DataType.BINARY_VECTOR, is_primary=False)
        schema.add_field("id", DataType.INT64, is_primary=True)

        self._client.create_collection(
            collection_name=self.table_name,
            schema=schema,
        )

    def _create_index(
        self,
        collection_name: str,
    ) -> None:
        index_params = MilvusClient.prepare_index_params()

        index_params.add_index(
            field_name="embedding",
            metric_type=self.metric_type,
            index_type=self.index_type,
            index_name=collection_name + "_index",
            params=self.index_params,
        )

        self._client.create_index(
            collection_name=collection_name,
            index_params=index_params,
        )

        logging.info(f"Index created for collection {collection_name}")

    def connect(self) -> Any:
        self._client = MilvusClient(self.db_uri)

    def initialize_meta_table(self) -> None:
        if not self._client.has_collection(self.METADATA_TABLE_NAME):
            logging.info(f"Creating Milvus collection {self.METADATA_TABLE_NAME}")

            schema = self._client.create_schema(enable_dynamic_field=True)
            schema.add_field("memoryset_table_name", DataType.VARCHAR, is_primary=True, max_length=256)
            schema.add_field("embedding_model_name", DataType.VARCHAR, is_primary=False, max_length=256)
            schema.add_field("embedding_model_version", DataType.INT64, is_primary=False)
            schema.add_field("embedding_model_embedding_dim", DataType.INT64, is_primary=False)
            schema.add_field("embedding_model_query_prompt", DataType.VARCHAR, is_primary=False, max_length=2048)
            schema.add_field("embedding_model_document_prompt", DataType.VARCHAR, is_primary=False, max_length=2048)

            self._client.create_collection(
                collection_name=self.METADATA_TABLE_NAME,
                schema=schema,
            )
        else:
            logging.info(f"Collection {self.METADATA_TABLE_NAME} already exists")

    def initialize_data_table(self, embedding_model_dim: int) -> None:
        if not self._client.has_collection(self.table_name):
            logging.info(f"Creating Milvus collection {self.table_name}")
            self._create_collection(embedding_model_dim)
            self._create_index(self.table_name)
        else:
            logging.info(f"Collection {self.table_name} already exists")

        self._client.load_collection(self.table_name)

    def write_metadata(self, embedding_model_config: EmbeddingModelConfig) -> None:
        if not self._client.has_collection(self.METADATA_TABLE_NAME):
            self.initialize_meta_table()

        self._client.insert(
            collection_name=self.METADATA_TABLE_NAME,
            data=[
                {
                    "memoryset_table_name": self.table_name,
                    "embedding_model_name": embedding_model_config.name,
                    "embedding_model_version": embedding_model_config.version,
                    "embedding_model_embedding_dim": embedding_model_config.embedding_dim or 0,
                    "embedding_model_query_prompt": embedding_model_config.query_prompt or "",
                    "embedding_model_document_prompt": embedding_model_config.document_prompt or "",
                }
            ],
        )

    def load_embedding_model_config(self) -> EmbeddingModelConfig | None:
        if not self._client.has_collection(self.METADATA_TABLE_NAME):
            return None
        row = self._client.query(
            collection_name=self.METADATA_TABLE_NAME,
            filter=f"memoryset_table_name == '{self.table_name}'",
            output_fields=[
                "embedding_model_name",
                "embedding_model_version",
                "embedding_model_embedding_dim",
                "embedding_model_query_prompt",
                "embedding_model_document_prompt",
            ],
        )

        if len(row) == 0:
            return None
        elif len(row) > 1:
            raise ValueError("found multiple metadata entries for memoryset")

        def empty_str_to_none(value: str) -> str | None:
            return None if value == "" else value

        def zero_to_none(value: int) -> int | None:
            return None if value == 0 else value

        return EmbeddingModelConfig(
            name=row[0]["embedding_model_name"],
            version=row[0]["embedding_model_version"],
            embedding_dim=zero_to_none(row[0]["embedding_model_embedding_dim"]),
            query_prompt=empty_str_to_none(row[0]["embedding_model_query_prompt"]),
            document_prompt=empty_str_to_none(row[0]["embedding_model_document_prompt"]),
        )

    def insert(self, data: list[MemoryToInsert]) -> None:
        data_to_insert = [self._prepare_for_insert(d) for d in data]
        self._client.insert(collection_name=self.table_name, data=data_to_insert)

    def lookup(self, query: np.ndarray, k: int, batch_size: int = 32) -> list[list[LabeledMemoryLookup]]:
        milvus_results = self._client.search(
            collection_name=self.table_name,
            data=query,
            limit=k,
            output_fields=["embedding", "label", "label_name", "metadata", "memory_version", "text", "image"],
            consistency_level="Strong",
            search_params={"metric_type": self.metric_type},
        )

        return [
            [self._to_labeled_memory_lookup(row, query[i]) for row in query_results]
            for i, query_results in enumerate(milvus_results)
        ]

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        result = self._client.query(
            collection_name=self.table_name,
            filter="id >= 0",
            output_fields=["embedding", "label", "label_name", "metadata", "memory_version", "text", "image"],
            limit=limit,
        )

        return [self._to_labeled_memory(row) for row in result]

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.to_list().__iter__()

    def __len__(self) -> int:
        result = self._client.query(collection_name=self.table_name, output_fields=["count(*)"])
        return result[0]["count(*)"]

    def drop_table(self):
        self._client.drop_collection(self.table_name)

    @classmethod
    def _to_labeled_memory_lookup(cls, row: dict[str, Any], query: np.ndarray) -> LabeledMemoryLookup:
        metadata_str = row["entity"]["metadata"]
        metadata = json.loads(metadata_str) if metadata_str is not None else {}
        embedding = np.array(row["entity"]["embedding"], dtype=np.float32)

        if row["entity"]["image"] is not None and row["entity"]["image"] != "":
            value = cls._decode_image(row["entity"]["image"])
        else:
            value = row["entity"]["text"]

        lookup_score = row["distance"]

        return LabeledMemoryLookup(
            embedding=embedding,
            label_name=MilvusStorageBackend._empty_to_none(row["entity"]["label_name"], str),
            label=row["entity"]["label"],
            lookup_score=lookup_score,
            memory_id=row["id"],
            memory_version=MilvusStorageBackend._empty_to_none(row["entity"]["memory_version"], str),
            metadata=metadata,
            value=value,
        )

    @classmethod
    def _to_labeled_memory(cls, row: dict[str, Any]) -> LabeledMemory:
        metadata_str = row["metadata"]
        metadata = json.loads(metadata_str) if metadata_str is not None else {}
        embedding = np.array(row["embedding"], dtype=np.float32)

        if row["image"] is not None and row["image"] != "":
            value = cls._decode_image(row["image"])
        else:
            value = row["text"]

        return LabeledMemory(
            embedding=embedding,
            label_name=MilvusStorageBackend._empty_to_none(row["label_name"], str),
            label=row["label"],
            memory_id=row["id"],
            memory_version=MilvusStorageBackend._empty_to_none(row["memory_version"], str),
            metadata=metadata,
            value=value,
        )
