# Smart Retail Surveillance — Full-Stack Edition

A full-stack AI retail analytics application with live YOLO object detection, MySQL persistence, a Flask analytics API, a React/Vite dashboard, explainable recommendations, and Docker Compose for local development.

## What is working

- React/Vite dashboard on `http://localhost:5173`
- Flask API on `http://localhost:5000`
- MySQL 8.4 in Docker, published to host port `3307`
- MySQL-backed `/api/health`, `/api/analytics`, `/api/events`, and `/api/recommendations`
- Sample detection data stored in `detection_events`
- Live YOLO11n + OpenCV detector on the Windows host using CPU PyTorch
- Detector can write either CSV events or live events directly to MySQL
- Explainable, rule-based retail recommendations

## Architecture

```text
Windows webcam
     ↓
YOLO11n + OpenCV (CPU)
     ↓
Detection events
     ├── CSV mode → data/detections.csv
     └── MySQL mode → MySQL detection_events
                         ↓
                    Flask API :5000
                         ↓
                    React :5173
```

The detector is intentionally kept outside the Flask Docker container. This keeps the API container lightweight and avoids pulling the large CUDA/NVIDIA dependency stack into the web service. CPU-only PyTorch is used for the Windows detector.

## 1. Docker full-stack setup

From `projects/smart-retail-surveillance`:

```bash
docker compose up -d
```

Services:

- MySQL: host `3307` → container `3306`
- Flask API: `5000`
- React/Vite: `5173`

Check status:

```bash
docker compose ps
```

Health check:

```bash
curl http://localhost:5000/api/health
```

PowerShell:

```powershell
Invoke-RestMethod http://localhost:5000/api/health
```

The expected health response reports `status=ok`, `service=smart-retail-api`, `storage=mysql`, and `database=connected`.

## 2. Verify MySQL data

The database schema is in `mysql/schema.sql`.

```bash
docker compose exec mysql mysql -usmart_retail -psmart_retail -e "USE smart_retail; SELECT COUNT(*) AS total_events FROM detection_events;"
```

The sample environment used during development contains 8 events: laptop ×3, cell phone ×2, book ×2, and mouse ×1.

## 3. API endpoints

- `GET /api/health` — API and database health
- `GET /api/analytics` — aggregate event counts, confidence and recommendations
- `GET /api/events?limit=100` — detection events
- `GET /api/recommendations` — explainable recommendations
- `POST /api/import-csv` — import the configured CSV into MySQL

Example:

```powershell
Invoke-RestMethod http://localhost:5000/api/events
```

## 4. Windows YOLO detector

The Flask Docker requirements intentionally do **not** install Ultralytics/OpenCV. Install detector dependencies into a separate Windows virtual environment:

```powershell
python -m venv .venv-detector
.\.venv-detector\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-detector.txt
```

The detector requirements use the CPU-only PyTorch wheel index. No NVIDIA CUDA runtime is required for the default CPU setup.

Verify:

```powershell
python -c "import torch; print(torch.__version__); print('CUDA:', torch.cuda.is_available())"
python -c "from ultralytics import YOLO; print('YOLO OK')"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
```

The first YOLO run downloads `yolo11n.pt` automatically if the model file is not already available.

### Live camera → MySQL

Make sure Docker MySQL is running, then run from the project root:

```powershell
.\.venv-detector\Scripts\Activate.ps1
python backend\live_detector.py --source 0 --storage mysql --mysql-host 127.0.0.1 --mysql-port 3307 --device cpu --confidence 0.4
```

The detector opens a window named `Smart Retail - YOLO Live Detection`. Press **Q** in that window to stop it.

Every detection batch is written to MySQL at most once per second by default. Use `--persist-every` to change this interval.

### CSV mode

To keep the original CSV workflow:

```powershell
python backend\live_detector.py --source 0 --storage csv --output data\detections.csv --device cpu
```

## 5. Detector options

```text
--source          Webcam index or video path (default: 0)
--model           YOLO model (default: yolo11n.pt)
--confidence      Minimum detection confidence (default: 0.4)
--device          Inference device (default: cpu)
--storage         mysql or csv (default: mysql)
--persist-every   Seconds between MySQL writes (default: 1.0)
--mysql-host      MySQL host (default: 127.0.0.1)
--mysql-port      MySQL host port (default: 3307)
--mysql-database  Database name
--mysql-user      Database user
--mysql-password  Database password
```

For a camera with poor lighting or small objects, try a lower threshold such as `--confidence 0.20`. Lower thresholds can increase detections but may also increase false positives.

## 6. Development notes

The backend uses a lightweight `backend/requirements.txt` containing Flask, CORS, Pandas, scikit-learn and MySQL Connector/Python. YOLO/OpenCV dependencies are isolated in `requirements-detector.txt` so Docker startup does not pull the large CUDA/NVIDIA dependency stack.

Do not run `docker compose down -v` unless you intentionally want to delete the MySQL volume and its stored data.

Do not repeatedly import the same CSV into MySQL unless duplicate event rows are intended.

## 7. Tests

```bash
PYTHONPATH=. python -m unittest backend.test_app
```

For a quick API smoke test:

```powershell
Invoke-RestMethod http://localhost:5000/api/health
Invoke-RestMethod http://localhost:5000/api/events
Invoke-RestMethod http://localhost:5000/api/analytics
```

## Privacy

The system stores event-level object detections. It does not implement face recognition, identity inference, demographic inference, emotion recognition, or hidden customer tracking.
