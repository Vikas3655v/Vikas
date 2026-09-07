# Smart Retail Surveillance — Full-Stack Edition

This is a full-stack AI retail application with live YOLO detection, CSV event capture, a Flask analytics API, a React dashboard, benchmarking, and MySQL persistence.

## Stack

- Frontend: React.js, JavaScript, HTML5, CSS3, Vite
- Backend/AI: Python, Flask, OpenCV, Ultralytics YOLO, Pandas, rule-based recommendations
- Data: CSV for capture/import; MySQL for persistent production-style storage
- DevOps: Git, GitHub, VS Code, Python venv, Docker Compose, GitHub Actions

## Architecture

Camera/video → YOLO/OpenCV live detector → CSV events → MySQL ingestion → Flask analytics API → React dashboard → explainable recommendations

The recommendation engine remains rule-based and transparent. It does not infer identity, demographics, emotions, or purchasing intent.

## 1. Quick CSV demo

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
set RETAIL_EVENTS=data/sample_detections.csv
# macOS/Linux: export RETAIL_EVENTS=data/sample_detections.csv
PYTHONPATH=. python backend/app.py
```

Then run the frontend:

```bash
cd frontend
npm install
npm run dev
```

## 2. Live YOLO mode

From the project directory:

```bash
PYTHONPATH=. python backend/live_detector.py --source 0 --output data/detections.csv
```

Press **q** to stop the camera. The detector writes timestamp, class, confidence, and bounding-box coordinates into the CSV.

## 3. MySQL-backed application

The application now supports `STORAGE_BACKEND=mysql`. The API reads events from MySQL instead of CSV when this mode is enabled.

### Option A — Docker Compose (recommended)

From this directory:

```bash
docker compose up
```

This starts:

- MySQL on port `3306`
- Flask API on port `5000`
- React/Vite on port `5173`

The MySQL container initializes `mysql/schema.sql` automatically.

### Import the detector CSV into MySQL

After MySQL and the API are running, call:

```bash
curl -X POST http://localhost:5000/api/import-csv
```

The API reads `RETAIL_EVENTS` and inserts the event rows into `detection_events`.

### Verify MySQL-backed analytics

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/analytics
curl http://localhost:5000/api/events?limit=100
```

`/api/health` reports `storage=mysql` and the database connection state. The analytics, events, and recommendation endpoints now read from MySQL in this mode.

## 4. Environment configuration

Copy `.env.example` values into your environment. Important variables:

```text
STORAGE_BACKEND=mysql
RETAIL_EVENTS=data/detections.csv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=smart_retail
MYSQL_USER=smart_retail
MYSQL_PASSWORD=smart_retail
MYSQL_POOL_SIZE=5
```

Do not commit real production database passwords or credentials.

## 5. Performance benchmark

```bash
PYTHONPATH=. python benchmark.py --events data/sample_detections.csv
```

This measures CSV load time, event throughput, and average detection confidence. True YOLO FPS/latency should be measured on the target machine because it depends on hardware and model configuration.

## 6. API

- `GET /api/health` — API and storage health
- `GET /api/analytics` — aggregate analytics and recommendations
- `GET /api/events?limit=100` — event rows
- `GET /api/recommendations` — explainable recommendation output
- `POST /api/import-csv` — import the configured CSV into MySQL; requires `STORAGE_BACKEND=mysql`

## 7. Tests and CI

```bash
PYTHONPATH=. python -m unittest backend.test_app
```

GitHub Actions compiles the Python modules and builds the React frontend for project changes.

## Privacy

The system stores event-level object detections. It does not implement face recognition, identity inference, demographic inference, emotion recognition, or hidden customer tracking.
