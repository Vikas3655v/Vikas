"""Lightweight activity-event aggregation over detector output.

This module deliberately does not claim semantic human activity recognition.
It converts repeated object detections into simple time-window events that can
be reviewed or used as input to a future labelled activity model.
"""

from __future__ import annotations

from collections import Counter


def summarize_detections(classes: list[str]) -> dict[str, int]:
    """Return counts by detected class."""
    return dict(Counter(item.strip().lower() for item in classes if item.strip()))


if __name__ == "__main__":
    print(summarize_detections(["person", "person", "laptop"]))
