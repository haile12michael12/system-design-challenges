# Day 2 - Global Weather Dashboard (Non-Functional Requirements Focus)

## Challenge Description
Build a weather app that must handle 1M users and 99.99% uptime. Goal: Document latency, availability, and scalability metrics.

## Project Structure
```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic models for data validation
│   ├── services.py      # Business logic and data services
│   ├── config.py        # Configuration management
│   ├── utils.py         # Utility functions
│   ├── monitoring.py    # Metrics collection and health checks
│   └── db.py            # Database connection placeholder
├── tests/
│   ├── test_models.py   # Tests for data models
│   └── test_services.py # Tests for business logic
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Multi-container Docker setup
├── nginx.conf           # Nginx reverse proxy configuration
├── Makefile             # Common development tasks
├── .env.sample          # Sample environment variables
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── ARCHITECTURE.md     # Architecture notes and design considerations
```

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable
- Implement non-functional requirements (scalability, availability, performance)

## Acceptance Criteria
- A runnable FastAPI starter in `app/main.py` that exposes a health endpoint
- `README.md` contains design prompts and next steps
- `ARCHITECTURE.md` with bullet points on components to design
- Dockerfile for containerization
- requirements.txt with dependencies
- Unit tests for models and services
- Monitoring endpoints for metrics collection

## Quickstart
```bash
cd day02

# Using virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Using Docker
docker build -t weather-dashboard .
docker run -p 8000:8000 weather-dashboard

# Using Docker Compose
docker-compose up --build

# Using Makefile
make setup
make dev
```

## API Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /hello` - Simple hello endpoint
- `GET /weather/{city}` - Get current weather for a city
- `GET /forecast/{city}` - Get weather forecast for a city
- `POST /preferences` - Set user preferences
- `GET /preferences/{user_id}` - Get user preferences
- `GET /metrics` - Get application metrics
- `GET /config` - Get application configuration

## Development
```bash
# Run tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Linting
make lint
```

## Next Steps
- Implement database models and persistence
- Add Redis caching for weather data
- Implement rate limiting
- Add authentication and authorization
- Implement background workers for data updates
- Add comprehensive logging
- Implement circuit breaker pattern
- Add load testing scripts
- Deploy to cloud platform (AWS, GCP, Azure)
