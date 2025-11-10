# Day 9 - Multi-Level Cache System

## Challenge Description
Implement API-level and DB-level caches (Redis + TTL + write-through). Goal: Master cache invalidation policies.

## Project Overview
This project implements a multi-level cache system with:
- FastAPI backend for REST API
- SQLAlchemy ORM with async support
- Redis for caching
- Background workers for cache management
- Monitoring and metrics collection

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## Directory Structure
```
day09/
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── core/
│ │ ├── config.py
│ │ └── logging_config.py
│ ├── routes/
│ │ ├── items.py
│ │ └── health.py
│ ├── db/
│ │ ├── __init__.py
│ │ ├── models.py
│ │ ├── session.py
│ │ └── migrations/
│ ├── cache/
│ │ ├── redis_client.py
│ │ ├── cache_utils.py
│ │ └── invalidation.py
│ ├── worker/
│ │ └── tasks.py
│ ├── monitoring/
│ │ ├── metrics.py
│ │ └── middlewares.py
│ ├── schemas.py
│ └── utils.py
├── tests/
│ ├── __init__.py
│ ├── test_items.py
│ └── conftest.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

## Quickstart

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (recommended)

### Using Docker Compose (Recommended)
```bash
cd day09
docker-compose up --build
```

### Local Development
```bash
cd day09
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints
- `GET /health/` - Health check
- `POST /items/` - Create item
- `GET /items/{id}` - Get item by ID
- `GET /items/` - List items
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## Testing
```bash
python -m pytest tests/ -v
```

## Next Steps
- Implement full cache layer with Redis
- Add cache invalidation policies
- Implement background workers for cache management
- Add monitoring and alerting
- Implement proper error handling and validation
- Add more unit and integration tests
- Implement cache warming strategies
