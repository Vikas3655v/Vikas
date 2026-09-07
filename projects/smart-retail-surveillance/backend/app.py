"""REST API for aggregate smart-retail analytics.

The API is intentionally event-level and non-identifying. It reads the same
CSV detection-event format produced by the object detector and exposes
aggregate analytics and explainable recommendations for the React dashboard.
"""

from __future__ import annotations

import csv
import os
from collections import Counter
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.recommend import build_recommendations

app = Flask(__name__)
CORS(app)

DEFAULT_EVENTS = Path(os.getenv("RETAIL_EVENTS", "data/detections.csv"))


def load_events(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "class" not in reader.fieldnames:
            raise ValueError("CSV must contain a 'class' column")
        return [row for row in reader if row.get("class")]


def summarize(events: list[dict[str, str]]) -> dict:
    categories = Counter((row.get("class") or "").strip().lower() for row in events)
    confidences = []
    for row in events:
        try:
            confidences.append(float(row.get("confidence", "")))
        except ValueError:
            continue

    return {
        "total_events": len(events),
        "unique_categories": len(categories),
        "average_confidence": round(sum(confidences) / len(confidences), 4) if confidences else None,
        "categories": dict(categories.most_common()),
        "recommendations": build_recommendations(categories),
    }


def events_path() -> Path:
    requested = request.args.get("events")
    return Path(requested) if requested else DEFAULT_EVENTS


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "smart-retail-api"})


@app.get("/api/analytics")
def analytics():
    try:
        events = load_events(events_path())
        return jsonify(summarize(events))
    except (OSError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.get("/api/events")
def event_rows():
    try:
        events = load_events(events_path())
        limit = min(max(request.args.get("limit", 100, type=int), 1), 1000)
        return jsonify({"count": len(events), "events": events[:limit]})
    except (OSError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.get("/api/recommendations")
def recommendations():
    try:
        events = load_events(events_path())
        categories = Counter((row.get("class") or "").strip().lower() for row in events)
        return jsonify({"recommendations": build_recommendations(categories)})
    except (OSError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
