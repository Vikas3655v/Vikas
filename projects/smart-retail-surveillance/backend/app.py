"""REST API for Smart Retail analytics with CSV and optional MySQL storage."""
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


def load_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "class" not in reader.fieldnames:
            raise ValueError("CSV must contain a 'class' column")
        return [row for row in reader if row.get("class")]


def summarize(events: list[dict]) -> dict:
    categories = Counter((row.get("class") or "").strip().lower() for row in events)
    confidences = []
    for row in events:
        try:
            confidences.append(float(row.get("confidence", "")))
        except (ValueError, TypeError):
            continue
    return {
        "total_events": len(events),
        "unique_categories": len(categories),
        "average_confidence": round(sum(confidences) / len(confidences), 4) if confidences else None,
        "categories": dict(categories.most_common()),
        "recommendations": build_recommendations(categories),
    }


def mysql_enabled() -> bool:
    return os.getenv("STORAGE_BACKEND", "csv").lower() == "mysql"


def get_store():
    from backend.mysql_store import MySQLStore
    return MySQLStore()


def current_events() -> list[dict]:
    if mysql_enabled():
        return get_store().fetch_events(min(max(request.args.get("limit", 1000, type=int), 1), 1000))
    return load_events(DEFAULT_EVENTS)


@app.get("/api/health")
def health():
    payload = {"status": "ok", "service": "smart-retail-api", "storage": "mysql" if mysql_enabled() else "csv"}
    if mysql_enabled():
        try:
            store = get_store()
            connection = store.connection()
            connection.close()
            payload["database"] = "connected"
        except Exception as exc:
            payload["status"] = "degraded"
            payload["database"] = "unavailable"
            payload["database_error"] = str(exc)
    return jsonify(payload)


@app.get("/api/analytics")
def analytics():
    try:
        return jsonify(summarize(current_events()))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.get("/api/events")
def event_rows():
    try:
        events = current_events()
        limit = min(max(request.args.get("limit", 100, type=int), 1), 1000)
        return jsonify({"count": len(events), "events": events[:limit]})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.get("/api/recommendations")
def recommendations():
    try:
        events = current_events()
        categories = Counter((row.get("class") or "").strip().lower() for row in events)
        return jsonify({"recommendations": build_recommendations(categories)})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/import-csv")
def import_csv():
    if not mysql_enabled():
        return jsonify({"error": "Set STORAGE_BACKEND=mysql before importing into MySQL"}), 400
    try:
        events = load_events(DEFAULT_EVENTS)
        inserted = get_store().insert_events(events)
        return jsonify({"inserted": inserted, "source": str(DEFAULT_EVENTS), "storage": "mysql"})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
