"""Predict a plant image using a saved Keras classifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf


def load_labels(model_path: Path) -> list[str]:
    """Load labels from either the transfer-learning JSON or baseline text file."""
    json_path = model_path.parent / "plant_disease_labels.json"
    text_path = model_path.with_suffix(".labels.txt")
    if json_path.exists():
        return json.loads(json_path.read_text(encoding="utf-8"))
    if text_path.exists():
        return text_path.read_text(encoding="utf-8").splitlines()
    raise FileNotFoundError(f"No label file found beside model: {model_path}")


def prepare_image(image_path: Path, model: tf.keras.Model) -> np.ndarray:
    """Prepare an image using the model's expected spatial size and preprocessing."""
    shape = model.input_shape
    if not isinstance(shape, tuple) or len(shape) != 4 or shape[1] is None or shape[2] is None:
        raise ValueError("Model must accept images with a fixed height and width")

    image_size = (int(shape[1]), int(shape[2]))
    image = tf.keras.utils.load_img(image_path, target_size=image_size)
    array = tf.keras.utils.img_to_array(image)

    # Transfer-learning model uses MobileNetV2 preprocessing; the small CNN
    # baseline uses an in-model Rescaling layer, so its raw pixel range is kept.
    first_layer = model.layers[0]
    if isinstance(first_layer, tf.keras.layers.InputLayer) and len(model.layers) > 1:
        first_layer = model.layers[1]
    if "mobilenet" in model.name.lower() or "mobilenet" in first_layer.name.lower():
        array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
    return np.expand_dims(array, axis=0)


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
    probabilities = model.predict(prepare_image(args.image, model), verbose=0)[0]
    top_indices = np.argsort(probabilities)[::-1][:args.top_k]

    print("Predictions:")
    for index in top_indices:
        label = labels[int(index)] if int(index) < len(labels) else f"class_{int(index)}"
        print(f"- {label}: {probabilities[int(index)] * 100:.2f}%")


if __name__ == "__main__":
    main()
