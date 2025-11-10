# Day 33 - Geo-Distributed Key-Value Store

## Challenge Description
Design a geo-distributed key-value store that provides low-latency access to data from multiple regions while maintaining consistency guarantees.

## Project Overview
This project implements a geo-distributed key-value store with:
- FastAPI backend for REST API
- PostgreSQL for persistent storage
- Redis for caching
- Consistent hashing for partitioning
- Vector clocks for conflict resolution
- Multiple consistency models (eventual, strong)

## Learning Goals
- Understand geo-distributed system design
- Implement consistency models and conflict resolution
- Apply consistent hashing for data partitioning
- Handle cross-region replication
- Manage vector clocks for causality tracking

## Directory Structure
```
day33/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── api/                    # API route handlers
│   │   ├── __init__.py
│   │   ├── health.py           # /health endpoint
│   │   ├── kv.py               # /kv CRUD endpoints
│   │   ├── replication.py      # /replicate, /sync routes
│   │   └── admin.py            # Admin & metrics
│   ├── core/                   # Core logic and settings
│   │   ├── config.py           # Env vars, region IDs, DB URLs
│   │   ├── consistency.py      # Consistency strategies
│   │   ├── hashing.py          # Consistent hashing & partitioning
│   │   └── vector_clock.py     # Vector clock utilities
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── session.py          # DB session management
│   │   ├── redis_cache.py      # Redis connection + caching utils
│   │   └── migrations/         # Alembic migrations
│   ├── workers/                # Background tasks
│   │   ├── __init__.py
│   │   ├── tasks.py            # Celery or RQ tasks
│   │   └── replication_worker.py # Handles async replication jobs
│   ├── utils/                  # Utility helpers
│   │   ├── logger.py           # Structured logging
│   │   ├── metrics.py          # Metrics setup
│   │   └── exceptions.py       # Custom exception handling
│   └── tests/                  # Unit & integration tests
│       ├── __init__.py
│       ├── test_health.py
│       ├── test_kv.py
│       ├── test_replication.py
│       └── test_partitioning.py
├── .env.example                # Example environment configuration
├── docker-compose.yml          # Multi-service setup (API, DB, Redis)
├── Dockerfile                  # FastAPI container definition
├── requirements.txt            # Python dependencies
├── README.md                   # Quickstart and usage
├── ARCHITECTURE.md             # Design components and trade-offs
└── Makefile                    # Helpful commands (test, run, lint)
```

## Quickstart

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (recommended)

### Using Docker Compose (Recommended)
```bash
cd day33
docker-compose up --build
```

### Local Development
```bash
cd day33
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints
- `GET /health/` - Health check
- `POST /kv/` - Create key-value pair
- `GET /kv/{key}` - Get key-value pair
- `PUT /kv/{key}` - Update key-value pair
- `DELETE /kv/{key}` - Delete key-value pair
- `POST /replicate/` - Replicate data between regions
- `POST /replicate/sync` - Sync region data
- `GET /admin/metrics` - Get system metrics
- `POST /admin/rebalance` - Rebalance cluster
- `GET /admin/regions` - List regions

## Testing
```bash
python -m pytest app/tests/ -v
```

## Next Steps
- Implement full replication logic
- Add conflict resolution with vector clocks
- Implement consistent hashing for data distribution
- Add monitoring and alerting
- Implement backup and restore functionality
- Add authentication and authorization
- Implement rate limiting
- Add compression for large values
