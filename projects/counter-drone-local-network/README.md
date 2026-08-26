# 🛡️ Advanced Counter-Drone System — Localized Network Monitoring

A defensive research prototype focused on **drone-detection telemetry and local-network monitoring**. The project is limited to detection, logging and analysis; it does not attempt to jam, hijack, disable or interfere with aircraft or radio communications.

## 🎯 Objective

Explore how a localized monitoring service can ingest telemetry records, detect suspicious patterns and generate alerts for human review.

## 📁 Structure

```text
counter-drone-local-network/
├── data/
│   └── sample_telemetry.csv   # Small demonstration dataset
├── src/
│   └── anomaly_detector.py   # Main analysis entry point
├── requirements.txt
└── README.md
```

## 🧪 Example Input

```csv
node_id,signal_strength,packet_rate,altitude
node-01,-42,18,85
node-02,-91,2,120
```

## ⚙️ Installation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run

```bash
python src/anomaly_detector.py --input data/sample_telemetry.csv
```

Custom thresholds:

```bash
python src/anomaly_detector.py \
  --input data/sample_telemetry.csv \
  --min-signal -80 \
  --min-packet-rate 5
```

## 🔍 Detection Logic

A record is flagged when both configured conditions are met:

```text
signal_strength < minimum signal
AND
packet_rate < minimum packet rate
```

This is a simple demonstration rule, not a production drone-detection algorithm.

## 🔐 Safety Boundary

This repository intentionally excludes signal jamming, spoofing, takeover, weaponization or instructions for interfering with aircraft.

## 🚀 Future Work

- Sensor fusion using multiple benign telemetry sources
- Time-series anomaly scoring
- Alert dashboard
- Offline evaluation using labelled telemetry
- Authentication and integrity checks for telemetry messages
