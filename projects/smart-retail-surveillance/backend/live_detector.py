"""Live YOLO detector that writes event-level detections to CSV."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

import cv2
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0", help="Webcam index or video path")
    parser.add_argument("--output", default="data/detections.csv")
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--confidence", type=float, default=0.4)
    args = parser.parse_args()

    source = int(args.source) if args.source.isdigit() else args.source
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    new_file = not output.exists() or output.stat().st_size == 0

    model = YOLO(args.model)
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {args.source}")

    with output.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["timestamp", "class", "confidence", "x1", "y1", "x2", "y2"])

        try:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                results = model.predict(frame, conf=args.confidence, verbose=False)
                annotated = results[0].plot()
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    x1, y1, x2, y2 = [round(float(v), 2) for v in box.xyxy[0].tolist()]
                    writer.writerow([
                        datetime.now(timezone.utc).isoformat(),
                        model.names[cls_id], confidence, x1, y1, x2, y2,
                    ])
                file.flush()
                cv2.imshow("Smart Retail - YOLO Live Detection", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            capture.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
