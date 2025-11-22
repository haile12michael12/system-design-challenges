# Day 19: Distributed File Storage System

A distributed file storage system with Write-Ahead Logging (WAL), replication, and recovery mechanisms.

## Features

- **File Storage**: Store, retrieve, and delete files with metadata
- **Write-Ahead Logging (WAL)**: Durability through write-ahead logging with checksums and segment rotation
- **Replication**: Synchronous and asynchronous replication to multiple replicas
- **Recovery**: WAL replay and bootstrap on startup
- **Telemetry**: Prometheus metrics and OpenTelemetry tracing
- **Containerization**: Docker and Docker Compose for easy deployment

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Primary       │    │   Replica 1      │    │   Replica 2      │
│   Storage       │◄──►│   Storage        │◄──►│   Storage        │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   WAL Service   │    │ Replication      │    │ Recovery         │
│   - Segments    │    │ Service          │    │ Service          │
│   - Checksums   │    │ - Sync           │    │ - Bootstrap      │
│   - Rotation    │    │ - Async Tasks    │    │ - WAL Replay     │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Health    │  │   Files     │  │        Admin            │ │
│  │   Routes    │  │   Routes    │  │       Routes            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Telemetry                               │
│  ┌─────────────┐  ┌──────────────────────────────────────────┐  │
│  │  Metrics    │  │              Tracing                     │  │
│  │ (Prometheus)│  │     (OpenTelemetry)                      │  │
│  └─────────────┘  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### Core Modules
- `config.py`: Application settings and environment loading
- `logging.py`: Structured JSON logging
- `security.py`: Security utilities (checksums, password hashing)

### API Routes
- `health.py`: Health and readiness checks
- `files.py`: File upload, download, and delete operations
- `admin.py`: Replica inspection and WAL inspection

### Database
- `models.py`: FileRecord and WALRecord models
- `session.py`: Database session management
- `repository.py`: CRUD helpers for metadata

### Services
- `wal_service.py`: WAL manager with checksums and segments
- `replication_service.py`: Synchronous and async replication
- `recovery_service.py`: WAL replay and bootstrap on startup

### Workers
- `replicator_worker.py`: Celery/RQ async replication

### Storage
- `local_store.py`: Local filesystem abstraction
- `object_store.py`: Placeholder S3/GCS store

### Telemetry
- `metrics.py`: Prometheus counters
- `tracing.py`: OpenTelemetry instrumentation

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.9+

### Running with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (required for Celery)
# You can use Docker for this:
docker run -d -p 6379:6379 redis:6-alpine

# Start the API server
python app/main.py

# In another terminal, start the Celery worker
celery -A app.workers.replicator_worker worker --loglevel=info

# In another terminal, start the Celery beat scheduler
celery -A app.workers.replicator_worker beat --loglevel=info
```

## API Endpoints

### Health Checks
- `GET /health` - Health check
- `GET /ready` - Readiness check

### File Operations
- `POST /upload` - Upload a file
- `GET /download/{file_id}` - Download a file
- `DELETE /files/{file_id}` - Delete a file

### Admin Operations
- `GET /admin/replicas/status` - Get replica status
- `GET /admin/wal/segments` - List WAL segments
- `GET /admin/wal/entries` - List WAL entries
- `POST /admin/replicas/sync` - Force replica synchronization
- `GET /admin/wal/inspect/{segment_id}` - Inspect WAL segment

## Scripts

- `scripts/load_test.py` - Load/performance testing script
- `scripts/repair_replicas.py` - Repair replica consistency

## Testing

```bash
# Run unit tests
pytest tests/

# Run specific test file
pytest tests/test_wal.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./sql_app.db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `STORAGE_PATH` | Primary storage path | `./data/primary` |
| `REPLICA1_PATH` | Replica 1 storage path | `./data/replica1` |
| `REPLICA2_PATH` | Replica 2 storage path | `./data/replica2` |
| `WAL_PATH` | WAL storage path | `./wal` |
| `DEBUG` | Debug mode | `False` |

## Project Structure

```
day19/
├─ app/
│ ├─ __init__.py
│ ├─ main.py                 # FastAPI app and routers registered
│ ├─ core/
│ │ ├─ config.py             # settings, environment loading
│ │ ├─ logging.py            # structured logging (JSON logs)
│ │ └─ security.py           # optional auth utilities
│ ├─ api/
│ │ ├─ __init__.py
│ │ ├─ deps.py               # shared dependencies
│ │ └─ routes/
│ │   ├─ health.py
│ │   ├─ files.py            # upload/download
│ │   └─ admin.py            # replica inspection, WAL inspection
│ ├─ db/
│ │ ├─ __init__.py
│ │ ├─ models.py             # FileRecord + WALRecord models
│ │ ├─ session.py            # future DB session creator
│ │ └─ repository.py         # CRUD helpers for metadata
│ ├─ services/
│ │ ├─ wal_service.py        # WAL manager w/ checksums & segments
│ │ ├─ replication_service.py # synchronous + async replication
│ │ └─ recovery_service.py   # WAL replay & bootstrap on startup
│ ├─ workers/
│ │ ├─ __init__.py
│ │ └─ replicator_worker.py  # Celery/RQ async replication
│ ├─ storage/
│ │ ├─ local_store.py        # local FS abstraction
│ │ └─ object_store.py       # placeholder S3/GCS store
│ └─ telemetry/
│   ├─ metrics.py            # Prometheus counters
│   └─ tracing.py            # OpenTelemetry instrumentation
│
├─ data/
│ ├─ primary/                # main storage
│ ├─ replica1/
│ └─ replica2/
├─ wal/
│ ├─ segments/               # rotated WAL segments
│ └─ wal.active              # active open WAL
│
├─ tests/
│ ├─ test_api.py
│ ├─ test_wal.py
│ ├─ test_replication.py
│ └─ test_recovery.py
│
├─ scripts/
│ ├─ load_test.py            # quick load/perf script
│ └─ repair_replicas.py
│
├─ README.md
├─ ARCHITECTURE.md
├─ Dockerfile
├─ docker-compose.yml        # API + Redis + worker
├─ requirements.txt
└─ pyproject.toml (optional)
```