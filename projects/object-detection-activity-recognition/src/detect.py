"""Run YOLO object detection and export structured detection events."""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import cv2
from ultralytics import YOLO


def parse_source(value: str) -> int | str:
    """Convert a numeric webcam index to int; otherwise return a path/URL."""
    return int(value) if value.isdigit() else value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="0", help="Webcam index or video path")
    parser.add_argument("--model", default="yolo11n.pt", help="YOLO model weights")
    parser.add_argument("--confidence", type=float, default=0.4, help="Minimum detection confidence")
    parser.add_argument("--output", type=Path, default=Path("results/detections.csv"))
    parser.add_argument("--no-display", action="store_true", help="Run without opening an OpenCV window")
    args = parser.parse_args()

    if not 0.0 < args.confidence <= 1.0:
        parser.error("--confidence must be between 0 and 1")

    capture = cv2.VideoCapture(parse_source(args.source))
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {args.source}")

    try:
        model = YOLO(args.model)
        args.output.parent.mkdir(parents=True, exist_ok=True)

        with args.output.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "class", "confidence", "x1", "y1", "x2", "y2"])

            while True:
                ok, frame = capture.read()
                if not ok:
                    break

                result = model.predict(frame, conf=args.confidence, verbose=False)[0]
                timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")

                for box in result.boxes:
                    class_id = int(box.cls.item())
                    confidence = float(box.conf.item())
                    x1, y1, x2, y2 = [round(float(value), 2) for value in box.xyxy[0].tolist()]
                    writer.writerow([timestamp, model.names[class_id], round(confidence, 4), x1, y1, x2, y2])

                if not args.no_display:
                    cv2.imshow("Object Detection", result.plot())
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
