# Smart Retail Surveillance — Full-Stack Edition

This enhancement turns the original event-processing prototype into a clearer full-stack portfolio project while preserving the privacy-first, explainable recommendation design.

## Stack

- Frontend: React.js, JavaScript, HTML5, CSS3, Vite
- Backend/AI: Python, OpenCV/YOLO detection pipeline, NumPy/Pandas-compatible analytics, rule-based recommendations
- Data: CSV event data and JSON API responses; MySQL is an optional production persistence layer and is not required by the current local implementation
- DevOps: Git, GitHub, VS Code, Python venv, Docker Compose, GitHub Actions

## Architecture

Camera/video → YOLO/OpenCV detector → CSV events → Python analytics API → React dashboard → explainable recommendations

The existing recommendation engine remains rule-based and transparent. It does not infer identity, demographics, emotions, or purchasing intent. The dashboard exposes aggregate event-level analytics only.

## Quick demo with included sample data

The repository includes `data/sample_detections.csv`, so the dashboard can be demonstrated immediately without a camera. To use it:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
set RETAIL_EVENTS=data/sample_detections.csv
# macOS/Linux: export RETAIL_EVENTS=data/sample_detections.csv
PYTHONPATH=. python backend/app.py
```

Then, in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://localhost:5173`).

## Backend

Start from the project directory. The API exposes:

- `GET /api/health` — service health
- `GET /api/analytics` — total events, unique categories, average confidence, category counts and recommendations
- `GET /api/events?limit=100` — event rows for inspection
- `GET /api/recommendations` — recommendation output

Set `RETAIL_EVENTS` to point to a different CSV file. The default remains `data/detections.csv` for compatibility with the object detector pipeline.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL` if the backend is not running at `http://localhost:5000`.

## Automated tests

Run the backend analytics test from the project directory:

```bash
PYTHONPATH=. python -m unittest backend.test_app
```

## Docker Compose

```bash
docker compose up
```

The React development server runs on port 5173 and the Python API on port 5000.

## CI/CD quality gate

`.github/workflows/smart-retail-ci.yml` automatically compiles the Python modules and builds the React frontend on pushes and pull requests that modify this project. The same workflow is the project's automated build gate; live workflow execution depends on the branch being pushed to a GitHub-enabled Actions environment.

## MySQL integration path

For a production deployment, MySQL can replace CSV as the persistent event store. A recommended schema is:

- `detection_events(id, timestamp, class_name, confidence, x1, y1, x2, y2)`
- indexes on `timestamp` and `class_name`
- aggregate queries for dashboard metrics

The current implementation deliberately keeps CSV as the portable local source of truth so the project remains easy to run without credentials or external services.
