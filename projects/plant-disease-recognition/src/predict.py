"""Predict a plant image using a saved Keras classifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf

IMAGE_SIZE = (160, 160)


def load_labels(model_path: Path) -> list[str]:
    """Load labels from either the JSON or text artifact beside a model."""
    json_path = model_path.parent / "plant_disease_labels.json"
    text_path = model_path.with_suffix(".labels.txt")
    if json_path.exists():
        return json.loads(json_path.read_text(encoding="utf-8"))
    if text_path.exists():
        return text_path.read_text(encoding="utf-8").splitlines()
    raise FileNotFoundError(f"No label file found beside model: {model_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    if not args.model.exists():
        raise FileNotFoundError(f"Model not found: {args.model}")
    if not args.image.exists():
        raise FileNotFoundError(f"Image not found: {args.image}")
    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    model = tf.keras.models.load_model(args.model)
    labels = load_labels(args.model)

    image = tf.keras.utils.load_img(args.image, target_size=IMAGE_SIZE)
    array = tf.keras.utils.img_to_array(image) / 255.0
    probabilities = model.predict(np.expand_dims(array, axis=0), verbose=0)[0]
    top_indices = np.argsort(probabilities)[::-1][:args.top_k]

    print("Predictions:")
    for index in top_indices:
        label = labels[int(index)] if int(index) < len(labels) else f"class_{int(index)}"
        print(f"- {label}: {probabilities[int(index)] * 100:.2f}%")


if __name__ == "__main__":
    main()
