# Day 18 - Latency-Aware News App

## Challenge Description
Choose between caching, prefetching, or batching for lowest perceived latency. Goal: Analyze UX vs backend trade-offs.

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## Acceptance Criteria
- A runnable FastAPI starter in `app/main.py` that exposes a health endpoint
- `README.md` contains design prompts and next steps
- `ARCHITECTURE.md` with bullet points on components to design
- Dockerfile for containerization
- requirements.txt with dependencies

## Quickstart

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (optional but recommended)

### Development Setup

1. **Create virtual environment:**
```bash
cd day18
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
uvicorn app.main:app --reload --port 8000
```

### Using Docker

1. **Start all services:**
```bash
cd infrastructure/docker
docker-compose up -d
```

2. **Access the services:**
- API: http://localhost:8000
- Database: postgres://localhost:5432
- Redis: redis://localhost:6379

### Running Tests
```bash
python -m pytest tests/ -v
```

## Project Structure
```
day18/
├─ app/
│ ├─ __init__.py
│ ├─ main.py
│ ├─ core/
│ │ ├─ config.py
│ │ └─ logging.py
│ ├─ api/
│ │ ├─ __init__.py
│ │ ├─ deps.py
│ │ └─ v1/
│ │ ├─ __init__.py
│ │ ├─ articles.py
│ │ └─ health.py
│ ├─ db/
│ │ ├─ __init__.py
│ │ ├─ models.py
│ │ ├─ session.py
│ │ └─ migrations/ (alembic placeholder)
│ ├─ services/
│ │ ├─ cache.py
│ │ ├─ news_service.py
│ │ └─ prefetch_service.py
│ └─ workers/
│ ├─ __init__.py
│ └─ tasks.py
├─ tests/
│ ├─ __init__.py
│ ├─ test_health.py
│ ├─ test_articles.py
│ └─ integration/
│ └─ test_endpoints.py
├─ infrastructure/
│ ├─ docker/
│ │ ├─ docker-compose.yml
│ │ ├─ redis.conf
│ │ └─ postgres-init.sql
├─ README.md
├─ ARCHITECTURE.md
├─ Dockerfile
└─ requirements.txt
```

## Key Features

### Caching
- Redis-based caching for articles
- Configurable cache TTL
- Automatic cache warming

### Prefetching
- User preference-based article prefetching
- Background prefetching tasks
- Configurable prefetch limits

### Background Workers
- Celery workers for async tasks
- Prefetching and cache warming tasks
- Separate worker queues

## Next Steps
- Implement real database integration
- Add user authentication
- Enhance prefetching algorithms
- Add more comprehensive monitoring
- Implement rate limiting
- Add data backup and recovery
