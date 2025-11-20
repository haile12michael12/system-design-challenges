# Day 12 - CAP Theorem Visualizer

## Challenge Description
Visualize the CAP theorem trade-offs between Consistency, Availability, and Partition tolerance in distributed systems.

## Project Structure
```
day12-fullstack/
├── backend/
│ ├── Dockerfile
│ ├── app/
│ │ ├── __init__.py
│ │ ├── main.py
│ │ ├── api/
│ │ │ ├── __init__.py
│ │ │ ├── health.py
│ │ │ └── cap.py
│ │ ├── db/
│ │ │ ├── __init__.py
│ │ │ ├── database.py
│ │ │ └── models.py
│ │ ├── core/
│ │ │ └── config.py
│ │ └── worker/
│ │ └── tasks.py
│ ├── requirements.txt
│ └── celeryconfig.py
├── frontend/
│ ├── Dockerfile
│ ├── package.json
│ ├── public/
│ │ └── index.html
│ └── src/
│ ├── index.jsx
│ │ └── App.jsx
│ └── api.js
├── docker-compose.yml
├── README.md
└── tests/
├── backend/
│ └── test_health.py
└── frontend/
└── test_ui.md
```

## Quickstart

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.11+ (for backend development)

### Running with Docker Compose
```bash
docker-compose up --build
```

### Running Locally (Backend)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Running Locally (Frontend)
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Health
- `GET /api/v1/health` - Health check endpoint

### CAP Simulation
- `POST /api/v1/cap/simulate` - Start a new CAP theorem simulation
- `GET /api/v1/cap/simulation/{simulation_id}` - Get simulation status

## Testing
```bash
cd backend
pytest
```