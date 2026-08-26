"""Train a YOLO detector from a standard Ultralytics dataset YAML."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Ultralytics dataset YAML")
    parser.add_argument("--model", default="yolo11n.pt", help="Base YOLO model")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--output-dir", type=Path, default=Path("runs"))
    args = parser.parse_args()

    if not args.data.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {args.data}")
    if args.epochs < 1 or args.imgsz < 32 or args.batch < 1:
        parser.error("epochs, imgsz and batch must be positive")

    model = YOLO(args.model)
    model.train(
        data=str(args.data),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=str(args.output_dir),
        name="detector",
    )


if __name__ == "__main__":
    main()
