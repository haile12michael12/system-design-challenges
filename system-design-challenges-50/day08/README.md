# Day 8 - Database Migration Simulator

## Challenge Description
Visualize the pain of migrating from SQL → NoSQL (or vice versa). Goal: CAP theorem + schema evolution.

## Project Overview
This project implements a database migration simulator with:
- FastAPI backend for REST API
- SQLAlchemy ORM with async support
- Alembic for database migrations
- Redis for caching
- Docker containerization

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## Directory Structure
```
day08/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI entrypoint with health endpoint
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py          # Health check route
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py             # SQLAlchemy engine + session setup
│   │   └── models.py              # Base SQLAlchemy models (Post, etc.)
│   │
│   ├── workers/
│   │   └── __init__.py            # (placeholder for Celery/RQ worker)
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis_client.py        # (optional Redis connection utility)
│   │
│   └── utils/
│       └── __init__.py            # (optional utilities, e.g., schema migration logic)
├── alembic/                       # (optional migration scripts)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 0001_init.py
├── tests/
│   ├── __init__.py
│   └── test_health.py             # basic unit test for health endpoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
└── .env.example                   # environment variables template
```

## Quickstart

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (recommended)

### Using Docker Compose (Recommended)
```bash
cd day08
docker-compose up --build
```

### Local Development
```bash
cd day08
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints
- `GET /v1/health/` - Health check

## Testing
```bash
python -m pytest tests/ -v
```

## Database Migrations
```bash
# Generate a new migration
alembic revision --autogenerate -m "migration message"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

## Next Steps
- Implement additional API endpoints
- Add more complex database models
- Implement caching with Redis
- Add background workers
- Implement proper error handling and validation
- Add more unit and integration tests
- Implement migration simulation logic
