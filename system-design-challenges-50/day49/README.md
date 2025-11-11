# Day 49 - Cost-Aware Autoscaler

## Challenge Description
Autoscale using cost + performance signals. Goal: Optimize cloud resource usage.

## Project Overview
This project implements a cost-aware autoscaler with:
- FastAPI backend for REST API
- SQLAlchemy ORM with async support
- Metrics simulation and collection
- Cost-based scaling decisions
- Dashboard for monitoring

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## Directory Structure
```
day49-cost-aware-autoscaler/
├─ README.md
├─ ARCHITECTURE.md
├─ requirements.txt
├─ Dockerfile
├─ .gitignore
├─ app/
│ ├─ __init__.py
│ ├─ main.py
│ ├─ api/
│ │ ├─ __init__.py
│ │ ├─ health.py
│ │ └─ dashboard.py
│ ├─ db/
│ │ ├─ __init__.py
│ │ ├─ models.py
│ │ └─ session.py
│ ├─ services/
│ │ ├─ autoscaler.py
│ │ ├─ metrics_simulator.py
│ │ ├─ metrics_exporter.py
│ │ └─ tests_autoscaler.py
│ └─ workers/
│ └─ scheduler.py
```

## Quickstart

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (recommended)

### Local Development
```bash
cd day49
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints
- `GET /health/` - Health check
- `GET /dashboard/metrics` - Get current metrics
- `GET /dashboard/status` - Get autoscaler status
- `POST /dashboard/scale` - Trigger manual scaling

## Testing
```bash
python -m pytest app/services/tests_autoscaler.py -v
```

## Next Steps
- Implement full metrics collection from real sources
- Add more sophisticated cost models
- Implement predictive scaling algorithms
- Add alerting and notification systems
- Implement proper error handling and validation
- Add unit and integration tests
- Add monitoring and logging
