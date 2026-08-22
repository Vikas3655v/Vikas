"""Evaluate a saved plant-disease classifier on a held-out directory."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 32
SEED = 42


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    args = parser.parse_args()

    dataset = tf.keras.utils.image_dataset_from_directory(
        args.data_dir,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )
    model = tf.keras.models.load_model(args.model)

    labels = dataset.class_names
    y_true = np.concatenate([y.numpy() for _, y in dataset], axis=0)
    probabilities = model.predict(dataset, verbose=0)
    y_pred = np.argmax(probabilities, axis=1)

    print(classification_report(y_true, y_pred, target_names=labels, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(y_true, y_pred))


if __name__ == "__main__":
    main()
