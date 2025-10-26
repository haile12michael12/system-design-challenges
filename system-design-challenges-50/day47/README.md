# Day 47 - Transactional Email Delivery Service

## Challenge Description
Transactional Email Delivery Service - Retries, deliverability, and metrics. Goal: Build reliable email systems.

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
```bash
cd day47
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Next Steps
- Expand the DB models in `app/db/models.py`
- Add caching with Redis where applicable
- Add a background worker using Celery or RQ
- Implement proper error handling and validation
- Add unit and integration tests
