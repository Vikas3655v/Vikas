"""Flag suspicious telemetry records for defensive monitoring."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def is_suspicious(row: dict[str, str], min_signal: float, min_packet_rate: float) -> bool:
    signal = float(row["signal_strength"])
    packet_rate = float(row["packet_rate"])
    return signal < min_signal and packet_rate < min_packet_rate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--min-signal", type=float, default=-80.0)
    parser.add_argument("--min-packet-rate", type=float, default=5.0)
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"node_id", "signal_strength", "packet_rate"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain: {', '.join(sorted(required))}")

        for row in reader:
            if is_suspicious(row, args.min_signal, args.min_packet_rate):
                print(f"ALERT: suspicious telemetry pattern from {row['node_id']}")


if __name__ == "__main__":
    main()
