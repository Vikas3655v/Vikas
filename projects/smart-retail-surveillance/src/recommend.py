"""Generate transparent retail recommendations from detection events."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

RULES = {
    "laptop": "Consider accessories such as a mouse or laptop sleeve.",
    "cell phone": "Consider phone accessories such as a case or charger.",
    "book": "Consider related books from the same category.",
}


def load_categories(path: Path) -> Counter[str]:
    """Load and normalize observed object categories from a detector CSV."""
    with path.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        if not rows.fieldnames or "class" not in rows.fieldnames:
            raise ValueError("Input CSV must contain a 'class' column")
        return Counter((row.get("class") or "").strip().lower() for row in rows if row.get("class"))


def build_recommendations(categories: Counter[str]) -> list[dict[str, object]]:
    """Create explainable recommendations for categories covered by RULES."""
    return [
        {
            "observed_category": category,
            "observations": count,
            "recommendation": RULES[category],
            "reason": "Rule matched to an observed category.",
        }
        for category, count in categories.most_common()
        if category in RULES
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, required=True, help="Detection CSV containing a class column")
    parser.add_argument("--output", type=Path, default=Path("results/recommendations.json"))
    args = parser.parse_args()

    if not args.events.exists():
        raise FileNotFoundError(f"Events file not found: {args.events}")

    categories = load_categories(args.events)
    report = {
        "observed_categories": dict(categories),
        "recommendations": build_recommendations(categories),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
