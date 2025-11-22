# Day 21: Social Media Platform API

A scalable social media platform API built with FastAPI, PostgreSQL, Redis, and Celery.

## Features

- User management (registration, authentication, profiles)
- Post creation and management
- Feed generation (personalized and explore)
- Media upload and processing
- Following/follower system
- Likes and bookmarks
- Background task processing with Celery
- Caching with Redis
- Dockerized deployment

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Caching**: Redis
- **Background Tasks**: Celery
- **Containerization**: Docker
- **Testing**: pytest

## Project Structure

```
app/
├── api/              # API endpoints
├── services/         # Business logic
├── repositories/     # Data access layer
├── schemas/          # Pydantic models
├── core/             # Core configuration and utilities
├── workers/          # Celery workers
├── db/               # Database models and session
├── utils/            # Utility functions
├── main.py           # Application entry point
tests/
├── api/              # API tests
├── services/         # Service tests
├── repositories/     # Repository tests
├── e2e/              # End-to-end tests
docker/               # Docker configurations
scripts/              # Utility scripts
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### Development Setup

1. Clone the repository
2. Copy `.env.sample` to `.env` and update values
3. Run the development environment:
   ```bash
   ./scripts/start_dev.sh
   ```

### Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start services:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d
   ```

3. Initialize database:
   ```bash
   ./scripts/init_db.sh
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

Run unit tests:
```bash
pytest tests/
```

## Deployment

For production deployment, use:
```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

## Environment Variables

See `.env.sample` for all required environment variables.

## License

This project is licensed under the MIT License.