# 🛍️ AI-Powered Smart Retail Surveillance & Personalized Recommendations

A modular prototype that connects computer-vision detection events with a transparent recommendation layer for retail analytics.

## Architecture

```text
Camera / Video
      ↓
Object Detection
      ↓
Detection Events (CSV)
      ↓
Category Aggregation
      ↓
Rule-Based Recommendation Engine
      ↓
Recommendation Report
```

The recommendation layer is intentionally **rule-based and explainable** in this version. It does not claim to infer customer identity, demographics, emotions, or purchasing intent.

## Features

- Read detection-event data produced by the object-detection project
- Aggregate observed categories
- Apply configurable product/category rules
- Produce an explainable recommendation report
- Keep surveillance and recommendation logic separate

## Run

```bash
python src/recommend.py --events data/detections.csv --output results/recommendations.json
```

## Input Format

The detector CSV should contain at least a `class` column. A minimal example is:

```csv
class
person
laptop
person
```

## Privacy

This prototype is designed around event-level data. Do not add face recognition, personally identifiable information, or hidden tracking without a clearly defined lawful purpose, appropriate consent/notice, and privacy controls.

## Future Improvements

- Replace rules with a validated recommendation model
- Add offline evaluation datasets
- Add confidence-aware event filtering
- Add a dashboard for aggregate, non-identifying analytics
- Measure recommendation precision/recall using a labelled evaluation set
