"""Summarize detector CSV events into simple, reviewable activity signals."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def summarize_detections(classes: list[str]) -> dict[str, int]:
    """Return normalized counts by detected class."""
    return dict(Counter(item.strip().lower() for item in classes if item.strip()))


def load_events(path: Path) -> dict[str, int]:
    """Load detection classes from the standard detector CSV."""
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "class" not in reader.fieldnames:
            raise ValueError("CSV must contain a 'class' column")
        return summarize_detections([row.get("class", "") for row in reader])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, help="Detection CSV produced by detect.py")
    args = parser.parse_args()

    if args.events:
        if not args.events.exists():
            raise FileNotFoundError(args.events)
        counts = load_events(args.events)
    else:
        counts = summarize_detections(["person", "person", "laptop"])

    print("Observed detection events:")
    for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"- {name}: {count}")


if __name__ == "__main__":
    main()
