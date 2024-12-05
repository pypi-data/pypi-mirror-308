from __future__ import annotations

import logging

from tqdm.auto import tqdm

from orcalib.rac.rac import RACModel

from .memory_types import DatasetLike
from .util import transform_data_to_dict_list
from .memoryset import LabeledMemoryset


def insert_useful_memories(
    memoryset: LabeledMemoryset,
    dataset: DatasetLike,
    model: RACModel,
    batch_size: int = 32,
    min_confidence: float = 0.85,
    log: bool = True,
) -> int:
    """
    Goes through each instance in the provided data and adds it to the memoryset ONLY if doing so will improve accuracy.

    NOTE: This method only works with text inputs for now!
    NOTE: This method is experimental. It may not work as expected, and it may be removed or changed in the future.
    """

    assert isinstance(model, RACModel), "Model must be an instance of RACModel"

    assert model is not None, "Model is required to determine which memories to add, but you provided None."
    assert (
        model.memoryset.table_name == memoryset.table_name
    ), f"Memorysets don't match: {model.memoryset.table_name} != {memoryset.table_name}"
    lookup_count = model.memory_lookup_count

    data = transform_data_to_dict_list(dataset, mode=memoryset.mode)

    insert_count = 0  # The number of rows we've actually inserted
    total_data_count = len(data)
    assert data and total_data_count > 0, "No data provided"

    # We need at least lookup_count memories in the memoryset in order to do any predictions.
    # If we don't have enough memories we'll add lookup_count elements to the memoryset.
    missing_mem_count = max(0, lookup_count - len(memoryset))
    if missing_mem_count:
        if len(data) <= missing_mem_count:
            if log:
                logging.info(
                    f"Memoryset needs a minimum of {missing_mem_count} memories for lookup, but only contains {len(memoryset)}."
                    f"{total_data_count}. Adding all {total_data_count} instances to the memoryset."
                )
            memoryset.insert(data, batch_size=batch_size, log=log)
            return total_data_count

        if log:
            logging.info(f"Adding {missing_mem_count} memories to reach minimum required count: {lookup_count}")

        memoryset.insert(data[:missing_mem_count], batch_size=batch_size, log=log)
        insert_count = missing_mem_count
        data = data[missing_mem_count:]

    assert len(data) > 0, "No data left to add to memoryset. This shouldn't be possible!"

    # Now we can start predicting and adding only the useful memories
    for row in tqdm(data, total=total_data_count - missing_mem_count):
        result = model.predict(row["text"], log=False)
        if result.label != row["label"] or result.confidence < min_confidence:
            memoryset.insert([row], log=log)
            insert_count += 1

    return insert_count
