# Real-Time Collaboration Editor

## Challenge Description
OT/CRDT basics and sync strategies. Goal: Implement collaborative editing features.

## Project Structure
```
app/
├── __init__.py
├── main.py # FastAPI app entrypoint
├── api/ # API layer (REST & WS)
│ ├── __init__.py
│ ├── routes/
│ │ ├── __init__.py
│ │ ├── health.py # /health endpoint
│ │ └── documents.py # CRUD endpoints for documents
│ └── ws/
│ ├── __init__.py
│ └── editor_ws.py # WebSocket endpoint for collaboration
│
├── core/ # Core utilities & protocols
│ ├── __init__.py
│ ├── config.py # Environment variables & settings
│ ├── ws_manager.py # WebSocket connection manager
│ ├── ot_engine.py # OT/CRDT logic placeholder
│ └── logger.py # Logging config
│
├── db/ # Persistence layer
│ ├── __init__.py
│ ├── models.py # SQLAlchemy models
│ ├── session.py # Async DB session helper
│ └── crud.py # CRUD functions for documents
│
├── workers/ # Background jobs (Celery/RQ)
│ ├── __init__.py
│ └── snapshot_worker.py # Periodic document snapshot task
│
├── services/ # Domain services (document sync, merge)
│ ├── __init__.py
│ └── sync_service.py # Merge + broadcast orchestration
│
└── tests/ # Unit & integration tests
 ├── __init__.py
 ├── test_health.py
 ├── test_ws_basic.py
 └── test_crud.py

migrations/ # Alembic migrations
└── versions/

scripts/ # DevOps / CLI tools
├── init_db.py
└── seed_data.py

docker/
├── Dockerfile # Container for app
├── docker-compose.yml # Local orchestration (API + Redis + DB + Worker)
└── entrypoint.sh
```

## Quickstart

### Using Docker (Recommended)
```bash
# Start all services
docker-compose -f docker/docker-compose.yml up --build

# Stop all services
docker-compose -f docker/docker-compose.yml down
```

### Local Development
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Seed database with sample data
python scripts/seed_data.py

# Run the application
uvicorn app.main:app --reload --port 8000
```

## Testing
```bash
# Run unit tests
python -m pytest app/tests/
```

## Environment Variables
Copy `.env.example` to `.env` and update the values as needed.

## Documentation
See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture information.
