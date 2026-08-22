"""Predict a plant image using a saved Keras model."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf

IMAGE_SIZE = (160, 160)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    args = parser.parse_args()

    if not args.model.exists():
        raise FileNotFoundError(f"Model not found: {args.model}")
    if not args.image.exists():
        raise FileNotFoundError(f"Image not found: {args.image}")

    model = tf.keras.models.load_model(args.model)
    labels_path = args.model.with_suffix(".labels.txt")
    labels = labels_path.read_text(encoding="utf-8").splitlines()

    image = tf.keras.utils.load_img(args.image, target_size=IMAGE_SIZE)
    array = tf.keras.utils.img_to_array(image)
    probabilities = model.predict(np.expand_dims(array, axis=0), verbose=0)[0]
    index = int(np.argmax(probabilities))

    print(f"Prediction: {labels[index]}")
    print(f"Confidence: {probabilities[index]:.4f}")


if __name__ == "__main__":
    main()
