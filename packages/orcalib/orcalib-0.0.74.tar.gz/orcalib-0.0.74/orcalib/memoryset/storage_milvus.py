from __future__ import annotations

import base64
import json
import logging
import os
from typing import Any, Iterator

import numpy as np
from PIL import Image
from pymilvus import DataType, MilvusClient

from .memory_types import LabeledMemory, LabeledMemoryLookup
from .storage import MemorysetMetadata, StorageBackend
from .util import MemoryToInsert, bytes_to_pil_image, pil_image_to_bytes

METRIC_TYPE = "IP"  # We always use inner product similarity because we use normalize embeddings


# TODO: Replace this once Milvus supports null values for scalar fields: https://github.com/milvus-io/milvus/issues/31728


def _none_to_empty(value: Any | None, klass) -> Any:
    if klass == str:
        return value if value is not None else ""
    elif klass == int:
        return value if value is not None else -1
    elif klass == float:
        return value if value is not None else float("nan")
    elif klass == dict:
        return value if value is not None else {}
    elif klass == list:
        return value if value is not None else []
    elif klass == bytes:
        return value if value is not None else ""
    else:
        raise ValueError(f"Unsupported class {klass}")


def _empty_to_none(value: Any, klass) -> Any:
    if klass == str:
        return value if value != "" else None
    elif klass == int:
        return value if value != -1 else None
    elif klass == float:
        return value if value != float("nan") else None
    elif klass == dict:
        return value if value != {} else None
    elif klass == list:
        return value if value != [] else None
    else:
        raise ValueError(f"Unsupported class {klass}")


def _encode_image(image: Image.Image) -> str:
    image_bytes = pil_image_to_bytes(image)
    image_str = base64.b64encode(image_bytes).decode("utf-8")
    return image_str


def _decode_image(image_str: str) -> Image.Image:
    image_bytes = base64.b64decode(image_str)
    return bytes_to_pil_image(image_bytes)


def _prepare_for_insert(datum: MemoryToInsert) -> dict[str, Any]:
    if datum["image"] is not None:
        image_str = _encode_image(datum["image"])
    else:
        image_str = ""

    return {
        "text": _none_to_empty(datum["text"], str),
        "image": image_str,
        "label": _none_to_empty(datum["label"], int),
        "label_name": _none_to_empty(datum["label_name"], str),
        "metadata": datum["metadata"] or "{}",
        "memory_version": _none_to_empty(datum["memory_version"], int),
        "embedding": _none_to_empty(datum["embedding"], list),
    }


def _to_labeled_memory_lookup(row: dict[str, Any], query: np.ndarray) -> LabeledMemoryLookup:
    metadata_str = row["entity"]["metadata"]
    metadata = json.loads(metadata_str) if metadata_str is not None else {}
    embedding = np.array(row["entity"]["embedding"], dtype=np.float32)

    if row["entity"]["image"] is not None and row["entity"]["image"] != "":
        value = _decode_image(row["entity"]["image"])
    else:
        value = row["entity"]["text"]

    lookup_score = row["distance"]

    return LabeledMemoryLookup(
        embedding=embedding,
        label_name=_empty_to_none(row["entity"]["label_name"], str),
        label=row["entity"]["label"],
        lookup_score=lookup_score,
        memory_id=row["id"],
        memory_version=_empty_to_none(row["entity"]["memory_version"], str),
        metadata=metadata,
        value=value,
    )


def _to_labeled_memory(row: dict[str, Any]) -> LabeledMemory:
    metadata_str = row["metadata"]
    metadata = json.loads(metadata_str) if metadata_str is not None else {}
    embedding = np.array(row["embedding"], dtype=np.float32)

    if row["image"] is not None and row["image"] != "":
        value = _decode_image(row["image"])
    else:
        value = row["text"]

    return LabeledMemory(
        embedding=embedding,
        label_name=_empty_to_none(row["label_name"], str),
        label=row["label"],
        memory_id=row["id"],
        memory_version=_empty_to_none(row["memory_version"], str),
        metadata=metadata,
        value=value,
    )


class MilvusStorageBackend(StorageBackend):
    METADATA_TABLE_NAME = "memoryset_metadata"

    def __init__(
        self,
        table_name: str,
        database_uri: str,
    ):
        super().__init__(table_name, database_uri)
        self.is_local_database = not database_uri.startswith("http")

    _connections: dict[str, MilvusClient] = {}

    @classmethod
    def _get_client(cls, database_uri: str, create: bool = False) -> MilvusClient | None:
        if database_uri.startswith("http") and not os.path.exists(database_uri) and not create:
            return None
        if database_uri not in cls._connections:
            cls._connections[database_uri] = MilvusClient(database_uri)
        return cls._connections[database_uri]

    def _drop_database(self):
        raise NotImplementedError("Milvus Lite does not support dropping databases")

    def _initialize_metadata_collection(self):
        client = self._get_client(self.database_uri)
        if client is None:
            return None
        if not client.has_collection(self.METADATA_TABLE_NAME):
            logging.info(f"Creating metadata table for {self.database_uri}")
            schema = client.create_schema(enable_dynamic_field=True)
            schema.add_field("memoryset_table_name", DataType.VARCHAR, is_primary=True, max_length=256)
            schema.add_field("embedding_dim", DataType.INT64, is_primary=False)
            schema.add_field("embedding_model_name", DataType.VARCHAR, is_primary=False, max_length=256)
            schema.add_field("embedding_model_version", DataType.INT64, is_primary=False)
            schema.add_field("embedding_model_query_prompt", DataType.VARCHAR, is_primary=False, max_length=2048)
            schema.add_field("embedding_model_document_prompt", DataType.VARCHAR, is_primary=False, max_length=2048)
            schema.add_field("embedding_model_max_seq_length", DataType.INT64, is_primary=False)
            client.create_collection(collection_name=self.METADATA_TABLE_NAME, schema=schema)
        else:
            # migrations will go here in the future
            pass

    def get_table_names(self) -> list[str]:
        client = self._get_client(self.database_uri)
        if client is None:
            return []
        self._initialize_metadata_collection()
        result = client.query(
            collection_name=self.METADATA_TABLE_NAME,
            output_fields=["memoryset_table_name"],
        )
        return [row["memoryset_table_name"] for row in result]

    def drop(self):
        client = self._get_client(self.database_uri)
        if client is None:
            logging.warning(f"Database not found at {self.database_uri}")
            return
        self.__client = None
        if not client.has_collection(self.table_name):
            logging.warning(f"Memoryset {self.table_name} not found in {self.database_uri}")
        else:
            client.drop_collection(self.table_name)
        client.delete(
            collection_name=self.METADATA_TABLE_NAME,
            filter=f"memoryset_table_name == '{self.table_name}'",
        )

    def get_metadata(self) -> MemorysetMetadata | None:
        client = self._get_client(self.database_uri)
        if client is None:
            return None
        self._initialize_metadata_collection()
        metadata = client.query(
            collection_name=self.METADATA_TABLE_NAME,
            filter=f"memoryset_table_name == '{self.table_name}'",
            output_fields=[
                "embedding_dim",
                "embedding_model_name",
                "embedding_model_version",
                "embedding_model_query_prompt",
                "embedding_model_document_prompt",
                "embedding_model_max_seq_length",
            ],
        )
        if len(metadata) == 0:
            return None
        elif len(metadata) > 1:
            raise ValueError("Found multiple metadata entries for memoryset")

        return MemorysetMetadata(
            embedding_dim=metadata[0]["embedding_dim"],
            embedding_model_name=metadata[0]["embedding_model_name"],
            embedding_model_version=_empty_to_none(metadata[0]["embedding_model_version"], int),
            embedding_model_query_prompt=_empty_to_none(metadata[0]["embedding_model_query_prompt"], str),
            embedding_model_document_prompt=_empty_to_none(metadata[0]["embedding_model_document_prompt"], str),
            embedding_model_max_seq_length=_empty_to_none(metadata[0]["embedding_model_max_seq_length"], int),
        )

    __client: MilvusClient | None = None

    @property
    def _client(self) -> MilvusClient:
        if self.__client is None:
            raise RuntimeError("You need to connect the storage backend before using it")
        return self.__client

    def _initialize_data_collection(self, embedding_dim: int) -> None:
        if not self._client.has_collection(self.table_name):
            logging.info(f"Creating collection {self.table_name}")
            schema = self._client.create_schema(auto_id=True, enable_dynamic_field=True)
            schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=embedding_dim, is_primary=False)
            schema.add_field("label", DataType.INT64, is_primary=False)
            schema.add_field("label_name", DataType.VARCHAR, is_primary=False, max_length=256)
            schema.add_field("metadata", DataType.VARCHAR, is_primary=False, max_length=2048)
            schema.add_field("memory_version", DataType.INT64, is_primary=False)
            schema.add_field("text", DataType.VARCHAR, is_primary=False, max_length=2048)
            # Milvus does not support storing bytes and varchar requires a max length, so to support
            # images for now, we set `enable_dynamic_field=True` and don't specify the image field
            # type. Images are stored as base64 encoded strings in this field for now. In the
            # future, we will probably switch to storing images separately and just storing a URI to
            # the image in this field.
            # schema.add_field("image", DataType.VARCHAR, is_primary=False, max_length=2048)
            schema.add_field("id", DataType.INT64, is_primary=True)
            self._client.create_collection(collection_name=self.table_name, schema=schema)
            # Create index
            logging.info(f"Creating index for collection {self.table_name}")
            index_params = MilvusClient.prepare_index_params()
            index_params.add_index(
                field_name="embedding",
                index_name=self.table_name + "_index",
                index_type="FLAT",  # We don't support other index types that need more config yet
                metric_type=METRIC_TYPE,
            )
            self._client.create_index(collection_name=self.table_name, index_params=index_params)
        self._client.load_collection(self.table_name)

    def _upsert_metadata(self, metadata: MemorysetMetadata) -> None:
        # if self._client
        self._initialize_metadata_collection()
        self._client.insert(
            collection_name=self.METADATA_TABLE_NAME,
            data=[
                {
                    "memoryset_table_name": self.table_name,
                    "embedding_dim": metadata.embedding_dim,
                    "embedding_model_name": metadata.embedding_model_name,
                    "embedding_model_version": _none_to_empty(metadata.embedding_model_version, int),
                    "embedding_model_max_seq_length": _none_to_empty(metadata.embedding_model_max_seq_length, int),
                    "embedding_model_query_prompt": _none_to_empty(metadata.embedding_model_query_prompt, str),
                    "embedding_model_document_prompt": _none_to_empty(metadata.embedding_model_document_prompt, str),
                }
            ],
        )

    def connect(self, metadata: MemorysetMetadata) -> MilvusStorageBackend:
        self.__client = self._get_client(self.database_uri)
        self.connected = True
        # TODO: add caching
        self._upsert_metadata(metadata)
        self._initialize_data_collection(embedding_dim=metadata.embedding_dim)
        return self

    def insert(self, data: list[MemoryToInsert]) -> None:
        data_to_insert = [_prepare_for_insert(d) for d in data]
        self._client.insert(collection_name=self.table_name, data=data_to_insert)

    def lookup(self, query: np.ndarray, k: int) -> list[list[LabeledMemoryLookup]]:
        # TODO: add caching
        milvus_results = self._client.search(
            collection_name=self.table_name,
            data=query.tolist(),
            limit=k,
            output_fields=["embedding", "label", "label_name", "metadata", "memory_version", "text", "image"],
            consistency_level="Strong",
            search_params={"metric_type": METRIC_TYPE},
        )
        return [
            [_to_labeled_memory_lookup(row, query[i]) for row in query_results]
            for i, query_results in enumerate(milvus_results)
        ]

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        result = self._client.query(
            collection_name=self.table_name,
            filter="id >= 0",
            output_fields=["embedding", "label", "label_name", "metadata", "memory_version", "text", "image"],
            limit=limit,
        )

        return [_to_labeled_memory(row) for row in result]

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.to_list().__iter__()

    def __len__(self) -> int:
        result = self._client.query(collection_name=self.table_name, output_fields=["count(*)"])
        return result[0]["count(*)"]
