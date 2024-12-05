import logging
import tempfile

import numpy as np
import pytest
from datasets import ClassLabel, Dataset

from .embedding_models import EmbeddingModel
from .memory_types import LabeledMemoryLookup, LookupReturnType
from .memoryset_v2 import LabeledMemorysetV2
from .storage_lancedb import LanceDBStorageBackend
from .storage_milvus import MilvusStorageBackend
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
TEST_DATA = [dict(value=SENTENCES[i], label=(i % 2), label_name=f"label_{i % 2}") for i in range(len(SENTENCES))]


BACKEND_TYPES = ["lancedb", "milvus"]

TEST_DATASET = Dataset.from_dict(
    {
        "text": SENTENCES,
        "label": [i % 2 for i in range(len(SENTENCES))],
    }
).cast_column("label", ClassLabel(names=["even", "odd"]))


@pytest.fixture()
def temp_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(params=BACKEND_TYPES)
def memoryset(request, temp_folder) -> LabeledMemorysetV2:
    match request.param:
        case "lancedb":
            uri = f"{temp_folder}/lance.db#memories"
        case "milvus":
            uri = f"{temp_folder}/milvus.db#memories"
        case _:
            raise ValueError(f"Unknown storage backend type: {request.param}")
    return LabeledMemorysetV2(uri, EmbeddingModel.CLIP_BASE)


def test_drop_and_exists(memoryset: LabeledMemorysetV2):
    # Given a memoryset
    assert LabeledMemorysetV2.exists(memoryset.uri)
    # When we drop the memoryset
    LabeledMemorysetV2.drop(memoryset.uri)
    # Then the memoryset no longer exists
    assert not LabeledMemorysetV2.exists(memoryset.uri)


@pytest.mark.parametrize("storage_backend_type", BACKEND_TYPES)
def test_create_new_memoryset(temp_folder, storage_backend_type):
    # When we create a new memoryset
    match storage_backend_type:
        case "lancedb":
            uri = f"{temp_folder}/lance.db#memories"
        case "milvus":
            uri = f"{temp_folder}/milvus.db#memories"
        case _:
            raise ValueError(f"Unknown storage backend type: {storage_backend_type}")
    memoryset = LabeledMemorysetV2(uri, EmbeddingModel.CLIP_BASE)
    # Then the correct storage backend is inferred from the URI
    match storage_backend_type:
        case "lancedb":
            assert isinstance(memoryset.storage_backend, LanceDBStorageBackend)
        case "milvus":
            assert isinstance(memoryset.storage_backend, MilvusStorageBackend)
        case _:
            raise ValueError(f"Unknown storage backend type: {storage_backend_type}")
    # And the embedding model is used
    assert memoryset.embedding_model == EmbeddingModel.CLIP_BASE
    # And the memoryset is empty
    assert len(memoryset) == 0


def test_reconnect_to_existing_memoryset(memoryset: LabeledMemorysetV2):
    # Given an existing memoryset with some memories
    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)
    memoryset_uri = memoryset.uri
    memoryset_embedding_model = memoryset.embedding_model
    del memoryset
    # When we reconnect to the memoryset
    reconnected_memoryset = LabeledMemorysetV2(memoryset_uri)
    # Then the memoryset with the correct embedding model is loaded
    assert reconnected_memoryset.embedding_model.config == memoryset_embedding_model.config
    # And it has the same number of memories
    assert len(reconnected_memoryset) == len(TEST_DATA)


def test_insert(memoryset: LabeledMemorysetV2):
    # When we insert memories into the memoryset
    memoryset.insert(TEST_DATA)
    # Then the memoryset has the correct number of memories
    assert len(memoryset) == len(TEST_DATA)
    # And all the memories are present
    contents = memoryset.to_list()
    assert len(contents) == len(TEST_DATA)
    for memory in contents:
        assert isinstance(memory, LabeledMemory)
        assert memory.value in SENTENCES
        assert memory.label in [0, 1]
        assert memory.label_name in [f"label_{i % 2}" for i in range(len(TEST_DATA))]


def test_insert_dataset(memoryset: LabeledMemorysetV2):
    # When a dataset is inserted into the memoryset
    memoryset.insert(TEST_DATASET)
    # Then the memoryset has the correct number of memories
    assert len(memoryset) == len(TEST_DATASET)
    # And the labels are correct
    assert all(memory.label in [0, 1, 2] for memory in memoryset.to_list())
    # TODO: ensure that label names are also populated


def test_lookup(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    # When we lookup 3 similar memories
    query = SENTENCES[np.random.randint(0, len(TEST_DATA))]
    result = memoryset.lookup(query, num_memories=3)
    # Then we get 3 similar memories
    assert len(result) == 3
    for lookup in result:
        assert isinstance(lookup, LabeledMemoryLookup)
        assert lookup.value in SENTENCES
        assert lookup.lookup_score > 0.5
        assert lookup.memory_id is not None
        assert lookup.memory_version is not None
        assert isinstance(lookup.embedding, np.ndarray)
        assert lookup.embedding.shape == (memoryset.embedding_model.embedding_dim,)
        assert lookup.embedding.dtype == np.float32


def test_lookup_columns(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    # When we lookup a batch of queries and request columnar results
    queries = [SENTENCES[np.random.randint(0, len(TEST_DATA))] for _ in range(3)]
    results = memoryset.lookup(queries, num_memories=5, return_type=LookupReturnType.COLUMNS)
    # Then we get back a dictionary containing the input embeddings as a list of numpy arrays
    assert isinstance(results["input_embeddings"], list)
    assert len(results["input_embeddings"]) == 3
    assert results["input_embeddings"][0].shape == (memoryset.embedding_model.embedding_dim,)
    assert results["input_embeddings"][0].dtype == np.float32
    # And the embeddings for the memories for each query as a list of list of numpy arrays
    assert isinstance(results["memories_embeddings"], list)
    assert len(results["memories_embeddings"]) == 3
    assert isinstance(results["memories_embeddings"][0], list)
    assert len(results["memories_embeddings"][0]) == 5
    assert results["memories_embeddings"][0][0].shape == (memoryset.embedding_model.embedding_dim,)
    assert results["memories_embeddings"][0][0].dtype == np.float32
    # And the values for the memories for each query
    assert isinstance(results["memories_values"], list)
    assert len(results["memories_values"]) == 3
    assert len(results["memories_values"][0]) == 5
    assert all(isinstance(value, str) for value in results["memories_values"][0])
    assert all(value in SENTENCES for value in results["memories_values"][0])
    # And the labels for the memories for each query
    assert isinstance(results["memories_labels"], list)
    assert len(results["memories_labels"]) == 3
    assert len(results["memories_labels"][0]) == 5
    assert all(label in [0, 1] for label in results["memories_labels"][0])
    # And the lookup scores for each query
    assert isinstance(results["memories_lookup_scores"], list)
    assert len(results["memories_lookup_scores"]) == 3
    assert len(results["memories_lookup_scores"][0]) == 5
    assert all(0 <= lookup_score <= 1.0 for lookup_score in results["memories_lookup_scores"][0])
    # And the memories ids for each query
    assert isinstance(results["memories_ids"], list)
    assert len(results["memories_ids"]) == 3
    assert len(results["memories_ids"][0]) == 5
    # And the memory versions for each query
    assert isinstance(results["memories_versions"], list)
    assert len(results["memories_versions"]) == 3
    assert len(results["memories_versions"][0]) == 5
    assert all(isinstance(memory_version, int) for memory_version in results["memories_versions"][0])
    # And the metadata for the memories for each query
    assert isinstance(results["memories_metadata"], list)
    assert len(results["memories_metadata"]) == 3
    assert len(results["memories_metadata"][0]) == 5
    assert all(isinstance(metadata, dict) for metadata in results["memories_metadata"][0])


def test_filter(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)
    # When we filter the memoryset to only include memories with the word "bird"
    destination_uri = memoryset.storage_backend.database_uri + "#filtered_table"
    filtered_memoryset = memoryset.filter(
        lambda x: "bird" in x.value if isinstance(x.value, str) else True,
        destination_uri,
    )
    # Then we get a new memoryset with the correct number of memories
    assert len(filtered_memoryset) == 5
    # And the old memoryset is unchanged
    assert len(memoryset) == len(TEST_DATA)


def test_map(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)
    # When we map the memoryset to a new memoryset with the words reversed
    destination_uri = memoryset.storage_backend.database_uri + "#mapped_table"
    reverse_words = lambda sentence: " ".join(reversed(sentence.split()))  # noqa: E731
    mapped_memoryset = memoryset.map(
        lambda x: dict(value=reverse_words(x.value) if isinstance(x.value, str) else x.value),
        destination_uri,
    )
    # Then we get a new memoryset with the correct number of memories
    assert len(mapped_memoryset) == len(TEST_DATA)
    # And the memories have the correct values
    assert all(x.value in [reverse_words(s) for s in SENTENCES] for x in mapped_memoryset.to_list())
    # And the old memoryset is unchanged
    assert len(memoryset) == len(TEST_DATA)
    assert all(x.value in SENTENCES for x in memoryset.to_list())
    # And the changed memories have been re-embedded
    assert all(x.embedding is not None for x in mapped_memoryset.to_list())
    # When we lookup a query that matches a mapped value exactly
    exact_match_query = "moon. the over flies chef The"
    assert exact_match_query in [x.value for x in mapped_memoryset.to_list()]
    # Then we get a perfect lookup score
    exact_match_result = mapped_memoryset.lookup(exact_match_query)
    assert exact_match_result[0].value == exact_match_query
    assert exact_match_result[0].lookup_score >= 0.999
    # When we lookup a query that doesn't match any of the mapped values
    other_query = "The chef flies over the moon."
    assert other_query not in [x.value for x in mapped_memoryset.to_list()]
    # Then we get a lookup score less than perfect
    other_result = mapped_memoryset.lookup(other_query)
    assert other_result[0].value != other_query
    assert other_result[0].lookup_score < 0.9


def test_clone(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)
    # When we clone it to a new memoryset
    destination_uri = memoryset.storage_backend.database_uri + "#destination_table"
    cloned_memoryset = memoryset.clone(destination_uri)
    # Then we get a new memoryset with the same number of memories
    assert len(cloned_memoryset) == len(TEST_DATA)
    # And the new memoryset has the same embedding model
    assert cloned_memoryset.embedding_model == memoryset.embedding_model
    # When we insert a new memory into the cloned memoryset
    cloned_memoryset.insert(dict(value="My new sentence", label=0, label_name="label_0"))
    # Then the new memoryset has one more memory than the original memoryset
    assert len(cloned_memoryset) == len(TEST_DATA) + 1
    # And the original memoryset is unchanged
    assert len(memoryset) == len(TEST_DATA)


def test_update_embedding_model(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)
    # When we clone it to a new memoryset and update the embedding model
    destination_uri = memoryset.storage_backend.database_uri + "#destination_table"
    new_embedding_model = EmbeddingModel.GTE_BASE
    cloned_memoryset = memoryset.clone(
        destination_uri,
        embedding_model=new_embedding_model,
    )
    # Then the new memoryset has the correct embedding model
    assert cloned_memoryset.embedding_model == new_embedding_model
    # And the embedding model is unchanged for the original memoryset
    assert memoryset.embedding_model == EmbeddingModel.CLIP_BASE
    # And the new memoryset has the correct number of memories
    assert len(cloned_memoryset) == len(TEST_DATA)
    # And the memories have been re-embedded
    assert all(x.embedding is not None for x in cloned_memoryset.to_list())
    for new_memory in cloned_memoryset.to_list():
        for old_memory in memoryset.to_list():
            if new_memory.value == old_memory.value:
                assert not np.allclose(new_memory.embedding, old_memory.embedding)
                break


def test_reset(memoryset: LabeledMemorysetV2):
    # Given a memoryset with some memories
    memoryset.insert(TEST_DATA)
    assert len(memoryset) == len(TEST_DATA)
    # When we reset the memoryset
    memoryset.reset()
    # Then the memoryset is empty
    assert len(memoryset) == 0
    # But we still have the same embedding model
    assert memoryset.embedding_model == EmbeddingModel.CLIP_BASE
    # And we can insert new memories
    memoryset.insert([dict(value="My new sentence", label=0, label_name="label_0")])
    assert len(memoryset) == 1
