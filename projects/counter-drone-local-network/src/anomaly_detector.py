"""Flag suspicious telemetry records for defensive monitoring."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED_COLUMNS = {"node_id", "signal_strength", "packet_rate"}


def is_suspicious(row: dict[str, str], min_signal: float, min_packet_rate: float) -> bool:
    """Return True when both configurable telemetry thresholds are crossed."""
    try:
        signal = float(row["signal_strength"])
        packet_rate = float(row["packet_rate"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("signal_strength and packet_rate must be numeric") from exc
    return signal < min_signal and packet_rate < min_packet_rate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Telemetry CSV")
    parser.add_argument("--min-signal", type=float, default=-80.0)
    parser.add_argument("--min-packet-rate", type=float, default=5.0)
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Telemetry file not found: {args.input}")

    with args.input.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = ", ".join(sorted(REQUIRED_COLUMNS - set(reader.fieldnames or [])))
            raise ValueError(f"CSV is missing required columns: {missing}")

        alerts = 0
        for row in reader:
            if is_suspicious(row, args.min_signal, args.min_packet_rate):
                alerts += 1
                print(f"ALERT: suspicious telemetry pattern from {row['node_id']}")

    print(f"Completed analysis: {alerts} alert(s)")


if __name__ == "__main__":
    main()
