# 🎯 Real-Time Object Detection & Activity Event Analysis

A computer-vision project for real-time object detection from a webcam or video source, with a lightweight event-analysis layer for reviewing detected objects.

## ✨ Features

- Webcam or video-file inference
- YOLO bounding boxes and confidence scores
- Configurable confidence threshold
- Timestamped detection-event CSV export
- Optional headless mode for servers/CI
- Simple event aggregation for later analysis
- Separate training entry point

## 🧰 Technologies

Python • OpenCV • Ultralytics YOLO

## 📁 Structure

```text
object-detection-activity-recognition/
├── data/
│   └── README.md              # Dataset setup; large datasets stay local
├── src/
│   ├── detect.py              # Main inference entry point
│   ├── train.py               # YOLO training entry point
│   └── activity.py            # Detection-event aggregation
├── results/                   # Generated CSV output; ignored by Git
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

## ▶️ Run Detection

Webcam:

```bash
python src/detect.py --source 0 --output results/detections.csv
```

Video file:

```bash
python src/detect.py --source path/to/video.mp4 --output results/detections.csv
```

Headless/server mode:

```bash
python src/detect.py --source path/to/video.mp4 --no-display --output results/detections.csv
```

## 📊 Analyze Detection Events

```bash
python src/activity.py --events results/detections.csv
```

## 🧠 Train a Custom Detector

Prepare an Ultralytics dataset YAML as described in `data/README.md`, then run:

```bash
python src/train.py --data data/retail.yaml --epochs 30
```

Generated training runs are stored under `runs/` and are not committed.

## 🔗 Project Pipeline

```text
Camera / Video
      ↓
YOLO Detection
      ↓
Detection Events (CSV)
      ↓
Activity/Event Aggregation
      ↓
Smart Retail Analytics (separate project)
```

## ⚠️ Scope & Limitations

The current implementation records **observable object detections**. It does not claim semantic human activity recognition such as fall detection or intent recognition. Detection quality depends on the model, camera, lighting, scene and hardware. Real-world security use requires domain-specific evaluation and privacy controls.

## 🚀 Future Improvements

- Add a labelled activity-recognition model
- Add tracking across frames
- Add configurable class filters
- Add automated evaluation metrics
- Add a small dashboard for aggregate results
