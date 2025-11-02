# Requirements Tracker Backend

This is the backend service for the Scalable Requirements Tracker built with FastAPI.

## Features

- RESTful API for requirements management
- User authentication and authorization
- Database operations with SQLAlchemy
- Database migrations with Alembic
- Caching with Redis
- Background task processing
- Comprehensive API documentation

## Tech Stack

- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- PostgreSQL (Relational database)
- Redis (In-memory cache)
- Uvicorn (ASGI server)
- Gunicorn (WSGI server for production)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Redis server

### Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy .env.example to .env and modify as needed):
   ```bash
   cp .env.example .env
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Production Deployment

For production deployment, use Gunicorn with Uvicorn workers:
```bash
gunicorn -c gunicorn_conf.py app.main:app
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI spec: http://localhost:8000/openapi.json

## Testing

Run tests with pytest:
```bash
python -m pytest tests/ -v
```

## Project Structure

```
app/
├── api/          # API routes
├── core/         # Core settings and startup logic
├── db/           # Database and migrations
├── models/       # SQLAlchemy ORM models
├── schemas/      # Pydantic models for request/response
├── services/     # Business logic / reusable service layer
├── workers/      # Background workers
├── main.py       # FastAPI entrypoint
└── dependencies.py  # Dependency injection
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `REDIS_HOST` - Redis server host
- `REDIS_PORT` - Redis server port
- `SECRET_KEY` - Secret key for JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration time

## Docker

Build and run with Docker:
```bash
docker build -t requirements-tracker-backend .
docker run -p 8000:8000 requirements-tracker-backend
```

## License

This project is licensed under the MIT License.