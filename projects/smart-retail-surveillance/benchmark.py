"""Lightweight benchmark for the retail analytics pipeline."""
from __future__ import annotations

import argparse
import csv
import statistics
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", default="data/sample_detections.csv")
    args = parser.parse_args()
    path = Path(args.events)
    start = time.perf_counter()
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    elapsed = time.perf_counter() - start
    confidences = [float(r["confidence"]) for r in rows if r.get("confidence")]
    throughput = len(rows) / elapsed if elapsed else 0
    print(f"Events: {len(rows)}")
    print(f"Load time: {elapsed * 1000:.2f} ms")
    print(f"Event throughput: {throughput:.2f} events/s")
    print(f"Average confidence: {statistics.mean(confidences):.4f}" if confidences else "Average confidence: n/a")


if __name__ == "__main__":
    main()
