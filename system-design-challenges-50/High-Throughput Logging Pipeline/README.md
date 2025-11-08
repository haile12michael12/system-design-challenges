# High-Throughput Logging Pipeline

## Challenge Description
Ingest, store, and query logs at scale. Goal: Build efficient logging infrastructure.

## Project Structure
```
app/
├── __init__.py
├── main.py                    # FastAPI entrypoint (health, lifespan, routers)
├── core/
│   ├── __init__.py
│   ├── config.py              # Settings (env vars, DB URL, Redis, secrets)
│   ├── logging_config.py      # Unified logging config (JSON logging)
│   └── exceptions.py          # Global error handlers & custom exceptions
├── db/
│   ├── __init__.py
│   ├── base.py                # SQLAlchemy Base & session factory
│   ├── models.py              # ORM models (LogEntry, Tenant, etc.)
│   └── migrations/            # Alembic migration scripts
├── schemas/
│   ├── __init__.py
│   ├── logs.py                # Pydantic schemas (LogIn, LogOut)
│   ├── query.py               # Schemas for search/filter endpoints
│   └── health.py              # Health response schemas
├── routers/
│   ├── __init__.py
│   ├── health.py              # /health endpoint
│   ├── ingest.py              # /ingest endpoint (async, batch)
│   ├── query.py               # /query endpoint (search/filter)
│   └── admin.py               # (optional) management routes
├── services/
│   ├── __init__.py
│   ├── redis_service.py       # Redis interface for queue ops
│   ├── db_service.py          # DB CRUD and bulk insert helpers
│   ├── log_ingestion.py       # Core ingestion logic (validate, buffer)
│   └── metrics_service.py     # Prometheus/OpenTelemetry hooks
├── workers/
│   ├── __init__.py
│   ├── redis_worker.py        # Async worker (polls Redis, writes to DB)
│   ├── celery_worker.py       # Optional Celery-based pipeline
│   └── retry_handler.py       # Retry/Backoff logic for failed inserts
├── utils/
│   ├── __init__.py
│   ├── time_utils.py          # Timestamp conversion, retention utils
│   ├── security_utils.py      # API key verification, JWT, hashing
│   └── compression_utils.py   # Optional gzip/snappy log compression
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_ingest.py
│   ├── test_query.py
│   └── test_worker.py
├── metrics/
│   └── instrumentator.py      # Prometheus Instrumentator config
├── __main__.py                # Allow running via `python -m app`
└── asgi.py                    # For deployment with ASGI servers

docker/
├── Dockerfile                 # FastAPI container
├── docker-compose.yml         # FastAPI + Redis + Postgres stack
└── worker.Dockerfile          # Worker service container

scripts/
├── load_test.py               # K6/wrk-like load generator (for testing throughput)
├── seed_db.py                 # Seed database for testing
└── migrate.sh                 # Simple migration script wrapper
```

## Quickstart

### Using Docker (Recommended)
```bash
# Start all services
make docker-up

# Stop all services
make docker-down
```

### Local Development
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Seed the database
make seed-db

# Run the application
make run

# Run the worker (in a separate terminal)
make run-worker
```

## Testing
```bash
# Run unit tests
make test

# Run load test
make load-test
```

## Linting
```bash
# Run linting
make lint
```

## Environment Variables
Copy `.env.example` to `.env` and update the values as needed.

## Documentation
See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture information.
