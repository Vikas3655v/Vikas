"""Train a YOLO detector from a standard Ultralytics dataset YAML.

Example:
python train.py --data data/retail.yaml --epochs 30
"""
from __future__ import annotations

import argparse
from pathlib import Path
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    args = parser.parse_args()

    if not args.data.exists():
        raise FileNotFoundError(args.data)

    model = YOLO(args.model)
    model.train(data=str(args.data), epochs=args.epochs, imgsz=args.imgsz, batch=args.batch, project="runs", name="detector")


if __name__ == "__main__":
    main()
