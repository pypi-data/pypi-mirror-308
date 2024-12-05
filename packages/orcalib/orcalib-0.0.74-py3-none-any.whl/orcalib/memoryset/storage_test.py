import logging
import random
import tempfile
from typing import Generator

import numpy as np
import pytest
from PIL import Image

from .embedding_models import EmbeddingModel
from .storage import MemorysetMetadata, StorageBackend
from .storage_lancedb import LanceDBStorageBackend
from .storage_milvus import MilvusStorageBackend
from .util import MemoryToInsert

logging.basicConfig(level=logging.INFO)


def _normalize(value):
    return value / np.linalg.norm(value)


def _random_monochrome_image(width: int = 800, height: int = 800):
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return Image.new("RGB", (width, height), (r, g, b))


def _images_are_close(image1: Image.Image, image2: Image.Image | None) -> bool:
    assert image2 is not None, "Image 2 is None"
    assert image1.size == image2.size, f"Image sizes do not match: {image1.size} != {image2.size}"
    array1 = np.array(image1)
    array2 = np.array(image2)
    return np.allclose(array1, array2, atol=2)


MEMORYSET_METADATA = MemorysetMetadata(
    embedding_model_name=EmbeddingModel.CLIP_BASE.name,
    embedding_model_version=EmbeddingModel.CLIP_BASE.version,
    embedding_dim=EmbeddingModel.CLIP_BASE.embedding_dim,
    embedding_model_query_prompt=EmbeddingModel.CLIP_BASE.config.query_prompt,
    embedding_model_document_prompt=EmbeddingModel.CLIP_BASE.config.document_prompt,
    embedding_model_max_seq_length=EmbeddingModel.CLIP_BASE.max_seq_length,
)
TEST_DATA_SIZE = 12
TEXT_DATA: list[MemoryToInsert] = [
    MemoryToInsert(
        text=f"text_{i}",
        label=(i % 2),
        label_name=f"label_{i % 2}",
        metadata="{}",
        embedding=list(_normalize(np.random.randn(MEMORYSET_METADATA.embedding_dim))),
        image=None,
        memory_version=1,
    )
    for i in range(TEST_DATA_SIZE)
]
IMAGE_DATA: list[MemoryToInsert] = [
    MemoryToInsert(
        text=None,
        label=(i % 2),
        label_name=f"label_{i % 2}",
        metadata="{}",
        embedding=list(_normalize(np.random.randn(MEMORYSET_METADATA.embedding_dim))),
        image=_random_monochrome_image(),
        memory_version=1,
    )
    for i in range(TEST_DATA_SIZE)
]


@pytest.fixture()
def temp_folder() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(params=["lancedb", "milvus"])
def unconnected_storage_backend(request, temp_folder) -> StorageBackend:
    match request.param:
        case "lancedb":
            return LanceDBStorageBackend(
                database_uri=f"{temp_folder}/lance.db",
                table_name="memories",
            )
        case "milvus":
            return MilvusStorageBackend(
                database_uri=f"{temp_folder}/milvus.db",
                table_name="memories",
            )
        case _:
            raise ValueError(f"Invalid storage backend: {request.param}")


@pytest.fixture()
def storage_backend(unconnected_storage_backend) -> StorageBackend:
    return unconnected_storage_backend.connect(MEMORYSET_METADATA)


def test_meta_tables(unconnected_storage_backend):
    # When getting metadata for a new storage backend that has never been connected
    metadata = unconnected_storage_backend.get_metadata()
    # Then the metadata is None
    assert metadata is None
    # When the storage backend is connected
    metadata = unconnected_storage_backend.connect(MEMORYSET_METADATA).get_metadata()
    # Then the metadata is not None anymore
    assert metadata is not None
    for m in metadata.__dict__.keys():
        assert getattr(metadata, m) == getattr(MEMORYSET_METADATA, m)
    # When reconnecting to the storage backend without connecting
    StorageBackendImplementation = unconnected_storage_backend.__class__
    database_uri = unconnected_storage_backend.database_uri
    table_name = unconnected_storage_backend.table_name
    del unconnected_storage_backend
    reconnected_storage_backend = StorageBackendImplementation(database_uri=database_uri, table_name=table_name)
    # Then the metadata is not None
    metadata = reconnected_storage_backend.get_metadata()
    assert metadata is not None


def test_reload_storage_backend(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == TEST_DATA_SIZE
    StorageBackendImplementation = storage_backend.__class__
    database_uri = storage_backend.database_uri
    table_name = storage_backend.table_name
    del storage_backend
    # When we reconnect to the storage backend
    reconnected_storage_backend = StorageBackendImplementation(
        database_uri=database_uri, table_name=table_name
    ).connect(MEMORYSET_METADATA)
    # Then we can access its memories
    assert len(reconnected_storage_backend) == TEST_DATA_SIZE


def test_drop_table(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == TEST_DATA_SIZE
    # When we drop the storage backend
    storage_backend.drop()
    # Then we can no longer access its memories
    with pytest.raises(RuntimeError):
        len(storage_backend)
    # When we re instantiate the storage backend
    StorageBackendImplementation = storage_backend.__class__
    database_uri = storage_backend.database_uri
    table_name = storage_backend.table_name
    del storage_backend
    reconnected_storage_backend = StorageBackendImplementation(database_uri=database_uri, table_name=table_name)
    # Then the storage backend does not exist anymore
    metadata = reconnected_storage_backend.get_metadata()
    assert metadata is None
    # And it has no memories after reconnecting
    assert len(reconnected_storage_backend.connect(MEMORYSET_METADATA)) == 0


def test_reset_storage_backend(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == TEST_DATA_SIZE
    # When we reset the storage backend
    storage_backend.reset(MEMORYSET_METADATA)
    # Then the storage backend is empty
    assert len(storage_backend) == 0


def test_to_list(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == TEST_DATA_SIZE
    # When we get the list of memories
    values = storage_backend.to_list()
    # Then we get a list of all the memories
    assert len(values) == TEST_DATA_SIZE
    # And the memories have the correct value, embedding, and embedding shape and type
    for value in values:
        assert isinstance(value.value, str)
        assert isinstance(value.embedding, np.ndarray)
        assert value.embedding.shape == (MEMORYSET_METADATA.embedding_dim,)
        assert value.embedding.dtype == np.float32


def test_insert_and_lookup_text(storage_backend):
    # Given a storage backend with some text memories
    storage_backend.insert(TEXT_DATA)
    # And a query vector
    i = np.random.randint(TEST_DATA_SIZE)
    query = np.array(TEXT_DATA[i]["embedding"]).reshape(1, -1)
    # When we look up the query vector
    memory_lookups = storage_backend.lookup(query, 4)
    # Then we get a list of lists of memories
    assert isinstance(memory_lookups, list)
    assert len(memory_lookups) == 1
    assert isinstance(memory_lookups[0], list)
    assert len(memory_lookups[0]) == 4
    # And the first memory in the list is the one with the matching text
    assert isinstance(memory_lookups[0][0].value, str)
    assert memory_lookups[0][0].value == TEXT_DATA[i]["text"]
    # And the lookup score is high
    assert memory_lookups[0][0].lookup_score >= 0.99
    # And the embedding is a numpy array of the correct shape and type
    assert isinstance(memory_lookups[0][0].embedding, np.ndarray)
    assert memory_lookups[0][0].embedding.shape == (MEMORYSET_METADATA.embedding_dim,)
    assert memory_lookups[0][0].embedding.dtype == np.float32


def test_insert_and_lookup_image(storage_backend):
    # Given a storage backend with some image memories
    storage_backend.insert(IMAGE_DATA)
    # And a query vector
    i = np.random.randint(TEST_DATA_SIZE)
    query_embedding = np.array(IMAGE_DATA[i]["embedding"]).reshape(1, -1)
    # When we look up the query vector
    memory_lookups = storage_backend.lookup(query_embedding, 1)
    # Then we get a list of lists of memories
    assert isinstance(memory_lookups, list)
    assert len(memory_lookups) == 1
    assert isinstance(memory_lookups[0], list)
    assert len(memory_lookups[0]) == 1
    # And the first memory in the list is the one with the matching image
    assert isinstance(memory_lookups[0][0].value, Image.Image)
    assert _images_are_close(memory_lookups[0][0].value, IMAGE_DATA[i]["image"])
    # And the lookup score is high
    assert memory_lookups[0][0].lookup_score >= 0.99


def test_storage_backend_equality():
    # Given two storage backends with the same database URI and table name
    storage_backend1 = LanceDBStorageBackend(database_uri="test", table_name="test")
    storage_backend2 = LanceDBStorageBackend(database_uri="test", table_name="test")
    # Then the storage backends are equal
    assert storage_backend1 == storage_backend2
