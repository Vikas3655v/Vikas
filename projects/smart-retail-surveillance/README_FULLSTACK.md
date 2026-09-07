# Smart Retail Surveillance — Full-Stack Edition

This enhancement turns the original event-processing prototype into a full-stack portfolio project with a live YOLO event pipeline, analytics API, React dashboard, benchmark utility, and optional MySQL persistence.

## Stack

- Frontend: React.js, JavaScript, HTML5, CSS3, Vite
- Backend/AI: Python, Flask, OpenCV, Ultralytics YOLO, Pandas, rule-based recommendations
- Data: CSV/JSON locally; MySQL persistence schema for production
- DevOps: Git, GitHub, VS Code, Python venv, Docker Compose, GitHub Actions

## Architecture

Camera/video → YOLO/OpenCV live detector → CSV events → Flask analytics API → React dashboard → explainable recommendations

Optional production path:

CSV/events → MySQL `detection_events` → analytics API → React dashboard

The recommendation engine remains rule-based and transparent. It does not infer identity, demographics, emotions, or purchasing intent.

## 1. Quick demo with sample data

From `projects/smart-retail-surveillance`:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
set RETAIL_EVENTS=data/sample_detections.csv
# macOS/Linux: export RETAIL_EVENTS=data/sample_detections.csv
PYTHONPATH=. python backend/app.py
```

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL (normally `http://localhost:5173`).

## 2. Live YOLO camera mode

The live detector is `backend/live_detector.py`. It opens a webcam, runs YOLO inference, displays annotated frames, and appends event rows to a CSV.

```bash
# from projects/smart-retail-surveillance
PYTHONPATH=. python backend/live_detector.py --source 0 --output data/detections.csv
```

Press **q** in the detector window to stop it. Start the Flask API against the same CSV in another terminal:

```bash
set RETAIL_EVENTS=data/detections.csv
# macOS/Linux: export RETAIL_EVENTS=data/detections.csv
PYTHONPATH=. python backend/app.py
```

Then refresh the React dashboard. The dashboard reads the current event file through the API.

## 3. API

- `GET /api/health` — service health
- `GET /api/analytics` — total events, unique categories, average confidence, category counts and recommendations
- `GET /api/events?limit=100` — event rows
- `GET /api/recommendations` — recommendation output

## 4. Performance benchmark

Run:

```bash
PYTHONPATH=. python benchmark.py --events data/sample_detections.csv
```

This measures CSV load time, event throughput, and average detection confidence. For true YOLO FPS/latency benchmarking, run the live detector on the target machine because inference speed depends on the hardware and model.

## 5. MySQL persistence

The `mysql/schema.sql` file creates the production event table with indexes on timestamp and class. The local demo intentionally remains credential-free and CSV-based.

```text
mysql/schema.sql
    ↓
smart_retail.detection_events
    ↓
future database-backed API
    ↓
React dashboard
```

## 6. Tests and CI

Run the backend unit tests:

```bash
PYTHONPATH=. python -m unittest backend.test_app
```

GitHub Actions compiles the Python modules and builds the React frontend for changes to this project. The workflow is defined in `.github/workflows/smart-retail-ci.yml`.

## Docker Compose

```bash
docker compose up
```

The development frontend runs on port 5173 and the API on port 5000.
