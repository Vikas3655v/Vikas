"""Live YOLO detector with CSV or MySQL event persistence."""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def csv_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def mysql_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run live YOLO detection and persist detection events.")
    parser.add_argument("--source", default="0", help="Webcam index or video path")
    parser.add_argument("--output", default="data/detections.csv", help="CSV output path when --storage=csv")
    parser.add_argument("--model", default="yolo11n.pt", help="Ultralytics YOLO model")
    parser.add_argument("--confidence", type=float, default=0.4, help="Minimum detection confidence")
    parser.add_argument("--device", default="cpu", help="Inference device, e.g. cpu or 0")
    parser.add_argument("--storage", choices=("csv", "mysql"), default=os.getenv("DETECTOR_STORAGE", "mysql"), help="Event persistence backend")
    parser.add_argument("--persist-every", type=float, default=1.0, help="Minimum seconds between MySQL writes")
    parser.add_argument("--mysql-host", default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    parser.add_argument("--mysql-port", type=int, default=int(os.getenv("MYSQL_PORT", "3307")))
    parser.add_argument("--mysql-database", default=os.getenv("MYSQL_DATABASE", "smart_retail"))
    parser.add_argument("--mysql-user", default=os.getenv("MYSQL_USER", "smart_retail"))
    parser.add_argument("--mysql-password", default=os.getenv("MYSQL_PASSWORD", "smart_retail"))
    args = parser.parse_args()

    source = int(args.source) if args.source.isdigit() else args.source
    model = YOLO(args.model)
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {args.source}")

    store = None
    csv_file = None
    writer = None
    last_persist = 0.0

    try:
        if args.storage == "mysql":
            os.environ.update({
                "MYSQL_HOST": args.mysql_host,
                "MYSQL_PORT": str(args.mysql_port),
                "MYSQL_DATABASE": args.mysql_database,
                "MYSQL_USER": args.mysql_user,
                "MYSQL_PASSWORD": args.mysql_password,
            })
            from backend.mysql_store import MySQLStore
            store = MySQLStore()
            print(f"MySQL storage enabled: {args.mysql_host}:{args.mysql_port}/{args.mysql_database}")
        else:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            new_file = not output.exists() or output.stat().st_size == 0
            csv_file = output.open("a", newline="", encoding="utf-8")
            writer = csv.writer(csv_file)
            if new_file:
                writer.writerow(["timestamp", "class", "confidence", "x1", "y1", "x2", "y2"])
            print(f"CSV storage enabled: {output}")

        while True:
            ok, frame = capture.read()
            if not ok:
                break

            results = model.predict(frame, conf=args.confidence, device=args.device, verbose=False)
            result = results[0]
            annotated = result.plot()
            events = []

            for box in result.boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = [round(float(v), 2) for v in box.xyxy[0].tolist()]
                events.append({
                    "timestamp": mysql_timestamp() if args.storage == "mysql" else csv_timestamp(),
                    "class": model.names[cls_id],
                    "confidence": confidence,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                })

            now = time.monotonic()
            if events and (args.storage == "csv" or now - last_persist >= args.persist_every):
                if store is not None:
                    inserted = store.insert_events(events)
                    print(f"Inserted {inserted} detection event(s) into MySQL")
                else:
                    writer.writerows([
                        [e["timestamp"], e["class"], e["confidence"], e["x1"], e["y1"], e["x2"], e["y2"]]
                        for e in events
                    ])
                    csv_file.flush()
                last_persist = now

            cv2.imshow("Smart Retail - YOLO Live Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()
        if csv_file is not None:
            csv_file.close()
        if store is not None:
            store.close()


if __name__ == "__main__":
    main()
