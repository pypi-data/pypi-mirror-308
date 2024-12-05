import logging
import tempfile
from typing import Generator

import numpy as np
import pytest
from datasets import ClassLabel, load_dataset

from .embedding_models import EmbeddingModel, EmbeddingModelConfig
from .memory_types import LabeledMemoryLookup
from .memoryset_v2 import LabeledMemorysetV2
from .storage import (
    LanceDBStorageBackend,
    MilvusStorageBackend,
    StorageBackend,
    StorageBackendType,
)
from .util import LabeledMemory

logging.basicConfig(level=logging.INFO)

SENTENCES = [
    "The chef flies over the moon.",
    "The cat fixes a theory.",
    "A bird brings the fence.",
    "The writer fixes the code.",
    "The student jumps over a mystery.",
    "A bird brings the mountain.",
    "The cat finds a theory.",
    "A bird teaches a new planet.",
    "The gardener cooks a puzzle.",
    "A bird throws a statue.",
    "A bird cooks a mystery.",
    "The artist finds a puzzle.",
    "A teacher throws the secret.",
    "The cat breaks a theory.",
    "A scientist finds the painting.",
    "The chef finds a statue.",
    "The robot paints an instrument.",
    "A dog sings to a new planet.",
    "The robot discovers the street.",
    "A scientist teaches a new planet.",
]

TEST_DATA = [
    LabeledMemory(
        value=SENTENCES[i],
        label=(i % 2),
        embedding=None,
        metadata={},
        label_name=f"label_{i % 2}",
        memory_version=1,
        memory_id=None,
    )
    for i in range(len(SENTENCES))
]


BACKEND_TYPES = list(StorageBackendType)


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
        raise ValueError(f"Unknown storage backend type: {storage_backend_type}")


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_create_memoryset(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    backend = storage_backend_factory(storage_backend_type, temp_folder)
    memoryset = LabeledMemorysetV2(backend, EmbeddingModel.GTE_BASE)

    assert memoryset.embedding_model.name == "Alibaba-NLP/gte-base-en-v1.5"
    assert memoryset.embedding_model.embedding_dim == 768


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_memoryset_insert_and_lookup(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    backend = storage_backend_factory(storage_backend_type, temp_folder)
    memoryset = LabeledMemorysetV2(backend, EmbeddingModel.GTE_BASE)

    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)

    contents = memoryset.to_list()
    assert len(contents) == len(TEST_DATA)

    random_index = np.random.randint(0, len(TEST_DATA))

    query = SENTENCES[random_index]
    result = memoryset.lookup(query, num_memories=1)

    assert len(result) == 1
    assert isinstance(result[0], LabeledMemoryLookup)
    assert result[0].value == query


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_memoryset_save_and_load(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    backend = storage_backend_factory(storage_backend_type, temp_folder)
    memoryset = LabeledMemorysetV2(backend, EmbeddingModel.GTE_BASE)

    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)

    uri = memoryset.storage_backend.uri_with_table_name

    del memoryset

    loaded_memoryset = LabeledMemorysetV2(uri, EmbeddingModel.GTE_BASE)

    assert len(loaded_memoryset) == len(TEST_DATA)

    assert loaded_memoryset.embedding_model.name == "Alibaba-NLP/gte-base-en-v1.5"
    assert loaded_memoryset.embedding_model.embedding_dim == 768

    random_index = np.random.randint(0, len(TEST_DATA))

    query = SENTENCES[random_index]
    result = loaded_memoryset.lookup(query, num_memories=1)

    assert len(result) == 1
    assert isinstance(result[0], LabeledMemoryLookup)
    assert result[0].value == query


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_filter_to_uri(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture

    source_backend = storage_backend_factory(storage_backend_type, temp_folder, table_name="source_table")
    source_memoryset = LabeledMemorysetV2(source_backend, EmbeddingModel.GTE_BASE)
    source_memoryset.insert(TEST_DATA)
    assert len(source_memoryset) == len(TEST_DATA)

    def filter_fn(x: LabeledMemory) -> bool:
        assert isinstance(x.value, str)
        return "bird" in x.value

    destination_uri = source_backend.uri_without_table_name + "#destination_table"
    filtered_memoryset = source_memoryset.filter(filter_fn, destination_uri)

    assert len(filtered_memoryset) == 5


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_filter_to_memoryset(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture

    source_backend = storage_backend_factory(storage_backend_type, temp_folder, table_name="source_table")
    source_memoryset = LabeledMemorysetV2(source_backend, EmbeddingModel.GTE_BASE)
    source_memoryset.insert(TEST_DATA)
    assert len(source_memoryset) == len(TEST_DATA)

    destination_backend = storage_backend_factory(storage_backend_type, temp_folder, table_name="destination_table")
    destination_memoryset = LabeledMemorysetV2(destination_backend, EmbeddingModel.GTE_BASE)

    def filter_fn(x: LabeledMemory) -> bool:
        assert isinstance(x.value, str)
        return "bird" in x.value

    filtered_memoryset = source_memoryset.filter(filter_fn, destination_memoryset)

    assert len(filtered_memoryset) == 5


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_map(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    source_backend = storage_backend_factory(storage_backend_type, temp_folder)
    source_memoryset = LabeledMemorysetV2(source_backend, EmbeddingModel.GTE_BASE)
    destination_uri = source_backend.uri_without_table_name + "#destination_table"

    source_memoryset.insert(TEST_DATA)
    assert len(source_memoryset) == len(TEST_DATA)

    def reverse_words(x: str) -> str:
        return " ".join(reversed(x.split()))

    def map_fn(x: LabeledMemory) -> dict:
        assert isinstance(x.value, str)
        return {
            "value": reverse_words(x.value),
        }

    mapped_memoryset = source_memoryset.map(map_fn, destination_uri)

    assert len(mapped_memoryset) == len(TEST_DATA)

    mapped_values = [x.value for x in mapped_memoryset.to_list()]

    assert "moon. the over flies chef The" in mapped_values

    query = "moon. the over flies chef The"

    result = mapped_memoryset.lookup(query, num_memories=1)
    assert len(result) == 1
    assert isinstance(result[0], LabeledMemoryLookup)
    assert result[0].value == query
    assert result[0].lookup_score >= 0.999

    query = "The chef flies over the moon."
    result = mapped_memoryset.lookup(query, num_memories=1)
    assert len(result) == 1
    assert isinstance(result[0], LabeledMemoryLookup)
    assert result[0].value != query
    assert result[0].lookup_score < 0.9


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_clone(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    source_backend = storage_backend_factory(storage_backend_type, temp_folder, table_name="source_table")
    source_memoryset = LabeledMemorysetV2(source_backend, EmbeddingModel.GTE_BASE)

    source_memoryset.insert(TEST_DATA)
    assert len(source_memoryset) == len(TEST_DATA)
    assert source_memoryset.storage_backend.table_name == "source_table"

    destination_uri = source_backend.uri_without_table_name + "#destination_table"
    cloned_memoryset = source_memoryset.clone(destination_uri)

    assert len(cloned_memoryset) == len(TEST_DATA)
    assert cloned_memoryset.storage_backend.uri_without_table_name == f"{temp_folder}/{storage_backend_type.value}.db"
    assert cloned_memoryset.storage_backend.table_name == "destination_table"

    cloned_memoryset.insert(
        LabeledMemory(
            value="My new sentence",
            label=0,
            embedding=None,
            metadata={},
            label_name="label_0",
            memory_version=1,
            memory_id=None,
        )
    )

    assert len(cloned_memoryset) == len(TEST_DATA) + 1
    assert len(source_memoryset) == len(TEST_DATA)


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_update_embedding_model(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    source_backend = storage_backend_factory(storage_backend_type, temp_folder, table_name="source_table")
    source_memoryset = LabeledMemorysetV2(source_backend, EmbeddingModel.GTE_BASE)
    destination_uri = source_backend.uri_without_table_name + "#destination_table"

    source_memoryset.insert(TEST_DATA)
    assert len(source_memoryset) == len(TEST_DATA)

    original_data = source_memoryset.to_list()

    destination_memoryset = source_memoryset.update_embedding_model(
        EmbeddingModel(EmbeddingModelConfig("roberta-base")), destination_uri
    )

    new_data = destination_memoryset.to_list()
    assert len(new_data) == len(TEST_DATA)

    for memory in new_data:
        assert memory.embedding is not None
        assert memory.embedding.shape == (768,)

        for old_memory in original_data:
            if memory.value == old_memory.value:
                assert not np.allclose(memory.embedding, old_memory.embedding)


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_insert_dataset(storage_backend_type: StorageBackendType, temp_folder_fixture):
    temp_folder = temp_folder_fixture
    backend = storage_backend_factory(storage_backend_type, temp_folder, table_name="source_table")
    memoryset = LabeledMemorysetV2(backend, EmbeddingModel.GTE_BASE)

    data = (
        load_dataset("osanseviero/twitter-airline-sentiment")["train"]
        .filter(lambda x: x["airline_sentiment_confidence"] == 1)
        .select_columns(["text", "airline_sentiment"])
        .rename_column("airline_sentiment", "label")
        .cast_column("label", ClassLabel(names=["negative", "neutral", "positive"]))
        .take(1000)
    )

    memoryset.insert(data)
    assert len(memoryset) == 1000
