"""Train an efficient transfer-learning plant disease classifier.

Designed for Google Colab or a local GPU. The dataset is expected to contain
one directory per class, as in PlantVillage.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import tensorflow as tf

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42


def build_model(num_classes: int) -> tf.keras.Model:
    base = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3), include_top=False, weights="imagenet"
    )
    base.trainable = False

    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x = tf.keras.layers.RandomFlip("horizontal")(inputs)
    x = tf.keras.layers.RandomRotation(0.08)(x)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("models"))
    parser.add_argument("--epochs", type=int, default=8)
    args = parser.parse_args()

    if not args.data_dir.exists():
        raise FileNotFoundError(args.data_dir)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        args.data_dir, validation_split=0.2, subset="training", seed=SEED,
        image_size=IMAGE_SIZE, batch_size=BATCH_SIZE
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        args.data_dir, validation_split=0.2, subset="validation", seed=SEED,
        image_size=IMAGE_SIZE, batch_size=BATCH_SIZE
    )

    model = build_model(len(train_ds.class_names))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = args.output_dir / "plant_disease_mobilenetv2.keras"
    labels_path = args.output_dir / "plant_disease_labels.json"

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=2, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(model_path, monitor="val_accuracy", save_best_only=True),
    ]
    history = model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)
    labels_path.write_text(json.dumps(train_ds.class_names, indent=2), encoding="utf-8")
    metrics = {
        "best_validation_accuracy": max(history.history.get("val_accuracy", [0.0])),
        "best_validation_loss": min(history.history.get("val_loss", [0.0])),
        "classes": train_ds.class_names,
    }
    (args.output_dir / "training_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
