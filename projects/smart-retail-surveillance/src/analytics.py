"""Aggregate retail detection events for simple, non-identifying analytics."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def load_classes(path: Path) -> Counter[str]:
    """Read a detector CSV and count normalized object classes."""
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "class" not in reader.fieldnames:
            raise ValueError("CSV must contain a 'class' column")
        return Counter((row.get("class") or "").strip().lower() for row in reader if row.get("class"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True, help="Detection CSV")
    args = parser.parse_args()

    if not args.events.exists():
        raise FileNotFoundError(f"Events file not found: {args.events}")

    counts = load_classes(args.events)
    print("Observed categories:")
    for name, count in counts.most_common():
        print(f"- {name}: {count}")


if __name__ == "__main__":
    main()
