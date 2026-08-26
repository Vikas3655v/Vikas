# 🛍️ AI-Powered Smart Retail Surveillance & Recommendations

A modular prototype that connects computer-vision detection events with transparent, rule-based recommendations for retail analytics.

## 🧩 Architecture

```text
Detection Events (CSV)
        ↓
Category Aggregation
        ↓
Rule-Based Recommendation Engine
        ↓
Recommendation Report (JSON)
```

The recommendation layer is intentionally **rule-based and explainable**. It does not claim to infer customer identity, demographics, emotions, or purchasing intent.

## ✨ Features

- Read object-detection event data
- Aggregate observed categories
- Apply explicit product/category rules
- Generate an explainable JSON report
- Keep analytics and recommendation logic separated

## 📁 Structure

```text
smart-retail-surveillance/
├── src/
│   ├── analytics.py           # Category counts
│   └── recommend.py           # Recommendation engine
├── results/                   # Generated JSON; ignored by Git
├── requirements.txt
└── README.md
```

## ⚙️ Installation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## 📥 Input

The detector CSV should contain at least a `class` column:

```csv
class
person
laptop
person
```

Generate the CSV from the [Object Detection project](../object-detection-activity-recognition/):

```bash
cd ../object-detection-activity-recognition
python src/detect.py --source 0 --output results/detections.csv
```

Then return to this project and use `../object-detection-activity-recognition/results/detections.csv` as the input file.

## 📊 Analytics

```bash
python src/analytics.py --events ../object-detection-activity-recognition/results/detections.csv
```

## 🤖 Recommendations

```bash
python src/recommend.py \
  --events ../object-detection-activity-recognition/results/detections.csv \
  --output results/recommendations.json
```

## 🔐 Privacy Boundary

This prototype works with event-level data. Do not add face recognition, personally identifiable information, or hidden tracking without a clearly defined lawful purpose, appropriate notice/consent and privacy controls.

## 🚀 Future Improvements

- Add confidence-aware event filtering
- Add offline evaluation datasets
- Replace rules with a validated recommendation model
- Add aggregate, non-identifying dashboards
- Measure recommendation quality with labelled evaluation data
