"""Run YOLO object detection on a webcam or video and export detection events."""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import cv2
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0", help="Webcam index or video path")
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--confidence", type=float, default=0.4)
    parser.add_argument("--output", type=Path, default=Path("results/detections.csv"))
    args = parser.parse_args()

    source: int | str = int(args.source) if args.source.isdigit() else args.source
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {args.source}")

    model = YOLO(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "class", "confidence", "x1", "y1", "x2", "y2"])

        try:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break

                result = model.predict(frame, conf=args.confidence, verbose=False)[0]
                annotated = result.plot()
                timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")

                for box in result.boxes:
                    cls = int(box.cls.item())
                    confidence = float(box.conf.item())
                    x1, y1, x2, y2 = [round(float(value), 2) for value in box.xyxy[0].tolist()]
                    writer.writerow([timestamp, model.names[cls], confidence, x1, y1, x2, y2])

                cv2.imshow("Object Detection", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            capture.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
