# Day 11 - Auto-Scaler Visualizer

## Challenge Description
Simulate vertical vs horizontal scaling with cost and latency graphs. Goal: Learn when to scale up/out.

## System Architecture
![System Diagram](docs/SYSTEM_DIAGRAM.png)

## Project Structure
```
day11/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── simulate.py
│   │   │   └── autoscaler.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging_config.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── services/
│   │   │   ├── autoscaler.py
│   │   │   ├── simulator.py
│   │   │   ├── metrics.py
│   │   │   └── cost_calculator.py
│   │   ├── workers/
│   │   │   ├── celery_app.py
│   │   │   └── tasks.py
│   │   └── utils/
│   │       └── scaling_helpers.py
│   │
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_simulator.py
│   │   └── test_autoscaler.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GraphLatencyCost.jsx
│   │   │   ├── AutoScaleControls.jsx
│   │   │   └── InstanceVisualizer.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── hooks/
│   │   │   └── useSimulationFetcher.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   ├── main.jsx
│   │   └── App.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── shared/
│   ├── types/
│   │   ├── scaling.ts
│   │   └── metrics.ts
│   └── utils/
│       └── constants.js
│
├── infra/
│   ├── docker-compose.yml
│   ├── k8s/
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── postgres.yaml
│   │   ├── redis.yaml
│   │   └── autoscaler-worker.yaml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── nginx/
│       ├── default.conf
│       └── Dockerfile
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── AUTOSCALING_LOGIC.md
│   └── SYSTEM_DIAGRAM.png
│
├── .env.example
└── README.md
```

## Quickstart

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.11+ (for backend development)

### Running with Docker Compose
```bash
cd infra
docker-compose up --build
```

### Running Locally (Backend)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Running Locally (Frontend)
```bash
cd frontend
npm install
npm run dev
```

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Autoscaling Logic](docs/AUTOSCALING_LOGIC.md)

## Testing
```bash
cd backend
pytest
```