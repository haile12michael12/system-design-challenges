# Day 3 - Feedback-Driven System Design Portal

## Challenge Description
Create a tool where users can submit design questions, and the system dynamically adjusts based on user feedback. Goal: Show evolving requirements and trade-offs.

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable
- Implement feedback collection and analytics

## File Structure
```
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── .env.sample
├── app/
│ ├── __init__.py
│ ├── main.py # FastAPI entrypoint
│ ├── db.py # SQLModel DB engine + session
│ ├── models.py # SQLModel models
│ ├── analytics.py # Analytics utilities and endpoints
│ └── scoring.py # Advanced scoring algorithm
├── tests/
│ ├── __init__.py
│ ├── test_questions.py
│ ├── test_feedback.py
│ └── test_analytics.py
├── docs/
│ └── DESIGN.md
├── Dockerfile
├── docker-compose.yml
└── k8s/
 ├── deployment.yaml
 ├── service.yaml
 └── hpa.yaml
```

## Acceptance Criteria
- A runnable FastAPI starter in `app/main.py` that exposes a health endpoint
- `README.md` contains design prompts and next steps
- `ARCHITECTURE.md` with bullet points on components to design
- Dockerfile for containerization
- requirements.txt with dependencies
- Tests for all major components
- Kubernetes deployment configurations
- Analytics and scoring implementation

## Quickstart
```bash
cd day03
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Running with Docker
```bash
cd day03
docker-compose up --build
```

## Running Tests
```bash
cd day03
pip install -r requirements-dev.txt
make test
```

## API Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /questions/` - Create a new question
- `GET /questions/` - Get all questions
- `GET /questions/{id}` - Get a specific question
- `POST /feedback/` - Submit feedback for a question
- `GET /feedback/{question_id}` - Get feedback for a question
- `POST /analytics/track-view/{question_id}` - Track a view
- `POST /analytics/track-feedback/{question_id}` - Track feedback
- `GET /analytics/{question_id}` - Get analytics for a question
- `GET /analytics/` - Get all analytics

## Next Steps
- Expand the DB models in `app/models.py`
- Add caching with Redis where applicable
- Add a background worker using Celery or RQ
- Implement proper error handling and validation
- Add unit and integration tests
- Deploy to Kubernetes cluster
- Add monitoring and alerting
- Implement CI/CD pipeline