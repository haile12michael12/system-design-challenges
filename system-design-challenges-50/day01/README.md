# Day 1 - Instagram Feed Service (Functional Requirements Focus)

## Challenge Description
Design a minimal Instagram feed system (no full app) where users see posts from people they follow. Goal: Extract and prioritize core functional requirements.

## Project Overview
This project implements an Instagram-like feed service with:
- FastAPI backend for REST API
- PostgreSQL for persistent storage
- Redis for caching
- Celery for background tasks
- SQLAlchemy ORM for database operations

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## Directory Structure
```
day01_instagram_feed/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes_feed.py      # /feed endpoints
│   │   ├── routes_health.py    # /health endpoint
│   │   └── routes_users.py     # (optional) user-related endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Environment variables, settings
│   │   ├── logger.py           # Logging configuration
│   │   └── utils.py            # Shared utilities
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # Base metadata for SQLAlchemy models
│   │   ├── models.py           # ORM models (Users, Posts, Follows)
│   │   ├── session.py          # DB connection setup
│   │   └── seeds.py            # (optional) sample data seeding
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── post_schema.py      # Pydantic models for Posts
│   │   └── user_schema.py      # Pydantic models for Users
│   ├── services/
│   │   ├── __init__.py
│   │   ├── feed_service.py     # Feed aggregation logic
│   │   ├── user_service.py     # User operations
│   │   └── cache_service.py    # Redis caching layer
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── tasks.py            # Celery tasks (e.g., fanout new posts)
│   │   └── celery_app.py       # Celery configuration
│   └── tests/
│       ├── __init__.py
│       ├── test_health.py
│       ├── test_feed.py
│       └── conftest.py         # Pytest fixtures
├── ARCHITECTURE.md             # Component overview + trade-offs
├── README.md                   # Quickstart & instructions
├── Dockerfile
├── requirements.txt
├── docker-compose.yml          # (optional) orchestrate Postgres + Redis + API
├── .env.example                # Example environment variables
├── .gitignore
└── Makefile                    # Helper commands (run, test, lint, etc.)
```

## Quickstart

### Prerequisites
- Python 3.9+
- Docker and Docker Compose (recommended)

### Using Docker Compose (Recommended)
```bash
cd day01
docker-compose up --build
```

### Local Development
```bash
cd day01
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints
- `GET /health/` - Health check
- `GET /feed/` - Get user's feed
- `GET /users/{user_id}` - Get user by ID
- `POST /users/{user_id}/follow/{target_user_id}` - Follow a user
- `POST /users/{user_id}/unfollow/{target_user_id}` - Unfollow a user

## Testing
```bash
python -m pytest app/tests/ -v
```

## Next Steps
- Implement full feed aggregation algorithm
- Add caching with Redis for improved performance
- Implement background workers for feed fanout
- Add authentication and authorization
- Implement rate limiting
- Add monitoring and logging
- Implement backup and restore functionality
