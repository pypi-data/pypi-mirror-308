"""Common type definitions and utility functions for the RAC module."""

from dataclasses import dataclass
from typing import Callable

import torch

from orcalib.memoryset import LabeledMemoryLookup


@dataclass
class PredictionResult:
    """
    The result of a single prediction.
    """

    label: int
    """The predicted label."""

    confidence: float
    """The confidence of the prediction."""

    memories: list[LabeledMemoryLookup]
    """The memory lookups that were used to guide this prediction."""

    logits: torch.Tensor
    """The logits of the prediction."""

    feedback: Callable[[int, int], float | int | bool] | None = None


@dataclass
class EvalResult:
    f1: float
    roc_auc: float | None
    accuracy: float
    loss: float


@dataclass
class LabeledMemoryLookupResult:
    correct: int
    incorrect: int
    label: int | None
    ratio: float | None
    total: int | None


@dataclass
class AnalyzePrediction:
    label: int
    logits: list[float]
    confidence: float


@dataclass
class AnalyzeResult:
    num_memories_accessed: int
    label_counts: dict[int, int]
    label_stats: list[dict]
    memory_stats: list[dict]
    mean_memory_lookup_score: float
    mean_memory_attention_weight: float
    prediction: AnalyzePrediction
