# 🎯 Real-Time Object Detection & Activity Recognition

A computer-vision application for real-time object detection from a webcam or video source, with a small event layer that records detected objects for later analysis.

## Features

- Webcam/video inference
- Object bounding boxes and confidence scores
- Configurable confidence threshold
- Timestamped detection events
- CSV export for simple analysis

## Technologies

Python • OpenCV • Ultralytics YOLO

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/detect.py --source 0 --output results/detections.csv
```

For a video file:

```bash
python src/detect.py --source path/to/video.mp4 --output results/detections.csv
```

The script uses a YOLO model configured with `--model`. A small pretrained model can be downloaded by the Ultralytics package when configured to do so; model weights are not committed to this repository.

## Activity Recognition Scope

The current implementation treats repeated object detections as observable events. Higher-level human activity recognition (for example, fall detection or specific actions) is intentionally separated as a future module rather than being claimed as implemented by the detector itself.

## Limitations

Detection quality depends on the model, camera, lighting, scene, and hardware. Real-world security use requires domain-specific evaluation and privacy considerations.
