import logging
import random
import tempfile
from typing import Generator

import numpy as np
import pytest
from PIL import Image

from .embedding_models import EmbeddingModel
from .storage import (
    LanceDBStorageBackend,
    MilvusStorageBackend,
    StorageBackend,
    StorageBackendType,
)
from .util import MemoryToInsert

logging.basicConfig(level=logging.INFO)


def _normalize(value):
    return value / np.linalg.norm(value)


def _random_monochrome_image(width: int = 800, height: int = 800):
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return Image.new("RGB", (width, height), (r, g, b))


def _images_are_close(image1: Image.Image, image2: Image.Image) -> bool:
    assert image1.size == image2.size, f"Image sizes do not match: {image1.size} != {image2.size}"
    array1 = np.array(image1)
    array2 = np.array(image2)
    return np.allclose(array1, array2, atol=2)


BACKEND_TYPES = list(StorageBackendType)

DIMENSION = EmbeddingModel.GTE_BASE.config.embedding_dim or 768
TEST_DATA_SIZE = 1000

TEST_DATA: list[MemoryToInsert] = [
    MemoryToInsert(
        text=f"text_{i}",
        label=(i % 2),
        label_name=f"label_{i % 2}",
        metadata="{}",
        embedding=list(_normalize(np.random.randn(DIMENSION))),
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
        embedding=list(_normalize(np.random.randn(DIMENSION))),
        image=_random_monochrome_image(),
        memory_version=1,
    )
    for i in range(TEST_DATA_SIZE)
]


@pytest.fixture()
def temp_folder_fixture() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(f"Creating backend at: {temp_dir}")
        yield temp_dir
        logging.info(f"Deleting backend from: {temp_dir}")


def storage_backend_factory(
    storage_backend_type: StorageBackendType, folder: str, table_name: str = "memories"
) -> StorageBackend:
    logging.info(f"Creating {storage_backend_type.value} backend at: {folder}")

    if storage_backend_type == StorageBackendType.LANCE_DB:
        return LanceDBStorageBackend(f"{folder}/{storage_backend_type.value}.db#{table_name}", EmbeddingModel.GTE_BASE)
    elif storage_backend_type == StorageBackendType.MILVUS:
        return MilvusStorageBackend(f"{folder}/{storage_backend_type.value}.db#{table_name}", EmbeddingModel.GTE_BASE)
    else:
        raise ValueError(f"Unsupported storage backend: {storage_backend_type}")


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_meta_tables(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    s = storage_backend_factory(storage_backend_type, temp_folder)

    assert s.uri_with_table_name == f"{temp_folder}/{storage_backend_type.value}.db#memories"
    assert s.table_name == "memories"
    assert s.embedding_model.name == EmbeddingModel.GTE_BASE.name

    loaded_config = s.load_embedding_model_config()
    assert loaded_config is not None
    assert loaded_config.name == EmbeddingModel.GTE_BASE.name


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_to_list(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    s = storage_backend_factory(storage_backend_type, temp_folder)

    s.insert(TEST_DATA)

    assert len(s) == TEST_DATA_SIZE

    values = s.to_list()

    assert len(values) == TEST_DATA_SIZE

    for i, value in enumerate(values):
        assert isinstance(value.value, str)
        assert isinstance(value.embedding, np.ndarray) and value.embedding.shape == (DIMENSION,)
        assert value.embedding.dtype == np.float32


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_insert_and_lookup(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    s = storage_backend_factory(storage_backend_type, temp_folder)

    s.insert(TEST_DATA)

    query_index = np.random.randint(TEST_DATA_SIZE)

    embedding = TEST_DATA[query_index]["embedding"]
    assert embedding is not None and isinstance(embedding, list) and len(embedding) == DIMENSION
    query = np.array(embedding).reshape(1, -1)
    assert query.shape == (1, DIMENSION)

    values = s.lookup(query, 4)
    assert len(values) == 1
    assert len(values[0]) == 4

    value = values[0][0]

    assert value.value == TEST_DATA[query_index]["text"]
    assert value.lookup_score >= 0.99
    assert isinstance(value.embedding, np.ndarray) and value.embedding.shape == (DIMENSION,)
    assert value.embedding.dtype == np.float32


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_reload_storage_backend(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    original_backend = storage_backend_factory(storage_backend_type, temp_folder)
    original_backend.insert(TEST_DATA)

    assert len(original_backend) == TEST_DATA_SIZE

    uri = original_backend.uri_without_table_name

    del original_backend

    if storage_backend_type == StorageBackendType.LANCE_DB:
        reloaded_backend: StorageBackend = LanceDBStorageBackend(uri)
    elif storage_backend_type == StorageBackendType.MILVUS:
        reloaded_backend: StorageBackend = MilvusStorageBackend(uri)

    assert len(reloaded_backend) == TEST_DATA_SIZE
    assert reloaded_backend.uri_without_table_name == uri
    assert reloaded_backend.table_name == "memories"
    assert reloaded_backend.embedding_model.name == EmbeddingModel.GTE_BASE.name


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_insert_images(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    s = storage_backend_factory(storage_backend_type, temp_folder)

    query_index = np.random.randint(TEST_DATA_SIZE)
    query_image = IMAGE_DATA[query_index]["image"]
    assert query_image is not None and isinstance(query_image, Image.Image)
    query_embedding = np.array(IMAGE_DATA[query_index]["embedding"]).reshape(1, -1)

    s.insert(IMAGE_DATA)
    assert len(s) == len(IMAGE_DATA)

    query_results = s.lookup(query_embedding, 1)

    assert len(query_results) == 1
    assert len(query_results[0]) == 1
    assert isinstance(query_results[0][0].value, Image.Image)
    assert _images_are_close(query_results[0][0].value, query_image)

    all_data = s.to_list()
    assert len(all_data) == TEST_DATA_SIZE
    assert isinstance(all_data[0].value, Image.Image)
