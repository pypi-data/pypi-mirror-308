from typing import cast

import numpy as np
import torch
from datasets import Dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    losses,
)
from sentence_transformers.training_args import (
    BatchSamplers,
    SentenceTransformerTrainingArguments,
)
from sklearn.metrics import f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
)

from .embedding_models import EmbeddingModel


class EmbeddingTrainingArguments(SentenceTransformerTrainingArguments):
    """Training arguments for finetuning an embedding model."""

    def __init__(
        self,
        output_dir: None = None,
        early_stopping_patience: int | None = None,
        early_stopping_threshold: float | None = None,
        per_device_train_batch_size: int = 32,
        per_device_eval_batch_size: int = 32,
        logging_steps: int = 5,
        **kwargs,
    ):
        """
        Initialize training arguments for finetuning an embedding model.

        Note:
            This class extends HuggingFace's [`TrainingArguments`][transformers.TrainingArguments],
            with sensible defaults and additional arguments for finetuning embedding models.
            For documentation of all available arguments, see that class.

        Args:
            output_dir: Do not set this, pass it as the first argument to the finetune method instead.
            early_stopping_patience: stop after this many epochs of no improvement on the `metric_for_best_model`
            early_stopping_threshold: stop if the specified `metric_for_best_model` is not improving by at least this much
        """
        if output_dir is not None:
            raise ValueError(
                "output_dir of training_args must not be set. Pass it as the first argument to the finetune method instead."
            )
        super().__init__(
            output_dir="/dev/null",
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            logging_steps=logging_steps,
            **kwargs,
        )
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_threshold = early_stopping_threshold


def finetune_for_classification(
    base_model: EmbeddingModel,
    output_dir: str,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    training_args: EmbeddingTrainingArguments = EmbeddingTrainingArguments(
        per_device_train_batch_size=32,
        per_device_eval_batch_size=32,
        gradient_accumulation_steps=2,
        num_train_epochs=2,
        eval_strategy="steps",
        save_strategy="steps",
        eval_steps=50,
        save_steps=50,
        early_stopping_patience=1,
        early_stopping_threshold=0.005,
        metric_for_best_model="eval_f1_score",
        greater_is_better=True,
        save_total_limit=2,
        load_best_model_at_end=True,
    ),
) -> EmbeddingModel:
    """
    Finetune the embedding model by adding a logistic regression head and training to predict labels

    Args:
        base_model: the embedding model to finetune
        output_dir: the directory to save the finetuned model to
        train_dataset: the dataset to use for training, must contain "value" and "label" features
        eval_dataset: the dataset to use for evaluation, must contain "value" and "label" features
        training_args: training arguments to use, if not given a default will be used

    Returns:
        A new finetuned embedding model
    """
    training_args.output_dir = output_dir
    training_args.prediction_loss_only = False  # reverse sentence transformer training args default
    training_args.remove_unused_columns = False  # needed for collator
    if training_args.early_stopping_patience is not None:
        early_stopping_callback = EarlyStoppingCallback(
            early_stopping_patience=training_args.early_stopping_patience,
            early_stopping_threshold=training_args.early_stopping_threshold,
        )
    else:
        early_stopping_callback = None
    assert train_dataset.features["value"].dtype == "string" and "label" in train_dataset.features
    assert eval_dataset.features["value"].dtype == "string" and "label" in eval_dataset.features

    num_labels = len(set(train_dataset["label"]))
    classification_model = AutoModelForSequenceClassification.from_pretrained(
        base_model.name,
        trust_remote_code=True,
        num_labels=num_labels,
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model.name)
    max_seq_length = min(
        max(len(tokenizer.tokenize(t)) for t in train_dataset["value"]),
        tokenizer.model_max_length,
    )

    def collate_fn(batch: list[dict]):
        tokens = tokenizer(
            [cast(str, b["value"]) for b in batch],
            padding="max_length",
            truncation=True,
            max_length=max_seq_length,
            return_tensors="pt",
        )
        batch_labels = torch.tensor([b["label"] for b in batch])
        return dict(**tokens, labels=batch_labels)

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=1)
        return dict(
            accuracy=(predictions == labels).mean(),
            f1_score=f1_score(labels, predictions, average="weighted" if num_labels > 2 else "binary"),
        )

    trainer = Trainer(
        model=classification_model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        callbacks=[early_stopping_callback] if early_stopping_callback else [],
        data_collator=collate_fn,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model(training_args.output_dir)
    tokenizer.save_pretrained(training_args.output_dir)
    return EmbeddingModel(
        training_args.output_dir,
        embedding_dim=base_model.embedding_dim,
        query_prompt=base_model.query_prompt,
        document_prompt=base_model.document_prompt,
    )


def finetune_with_triplets(
    base_model: EmbeddingModel,
    output_dir: str,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    training_args: EmbeddingTrainingArguments = EmbeddingTrainingArguments(
        per_device_train_batch_size=64,
        per_device_eval_batch_size=64,
        gradient_accumulation_steps=2,
        num_train_epochs=1,
        eval_strategy="epoch",
        save_strategy="epoch",
        batch_sampler=BatchSamplers.GROUP_BY_LABEL,
    ),
) -> EmbeddingModel:
    """
    Finetune the embedding model via contrastive triplet loss based on labels

    Args:
        base_model: the embedding model to finetune
        output_dir: the directory to save the finetuned model to
        train_dataset: the dataset to use for training, must contain "value" and "label" features
        eval_dataset: the dataset to use for evaluation, must contain "value" and "label" features
        training_args: training arguments to use, if not given a default will be used

    Returns:
        A new finetuned embedding model
    """
    try:
        model = SentenceTransformer(base_model.name, trust_remote_code=True)
    except Exception as e:
        raise ValueError("triplet finetuning only works with models that are compatible with SentenceTransformer", e)

    training_args.output_dir = output_dir
    if training_args.batch_sampler != BatchSamplers.GROUP_BY_LABEL:
        raise ValueError("batch_sampler cannot be overridden for triplet finetuning")
    assert train_dataset.features["value"].dtype == "string" and "label" in train_dataset.features
    assert eval_dataset.features["value"].dtype == "string" and "label" in eval_dataset.features
    train_dataset.rename_column("value", "sentence")
    # set max sequence length to the longest sentence in the training dataset
    model.max_seq_length = min(
        max(len(model.tokenizer.tokenize(t)) for t in train_dataset["value"]),
        model.max_seq_length,
    )

    trainer = SentenceTransformerTrainer(
        model=model,
        loss=losses.BatchHardSoftMarginTripletLoss(model),
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    trainer.train()
    trainer.save_model(training_args.output_dir)
    return EmbeddingModel(
        training_args.output_dir,
        embedding_dim=base_model.embedding_dim,
        query_prompt=base_model.query_prompt,
        document_prompt=base_model.document_prompt,
    )
