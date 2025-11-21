# E-Commerce Platform - Day 14

A comprehensive e-commerce platform built with FastAPI, featuring catalog management, order processing, user authentication, and payment handling.

## Features

- Product catalog management
- User authentication and authorization
- Order processing system
- Payment integration
- Background task processing
- Caching with Redis
- Event-driven architecture
- Containerized with Docker
- Kubernetes deployment ready
- CI/CD pipelines

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional, for containerization)
- PostgreSQL (or use Docker Compose)
- Redis (or use Docker Compose)

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (copy `.env.example` to `.env` and modify as needed)

### Running the Application

#### Local Development

```bash
uvicorn app.main:app --reload
```

#### With Docker Compose

```bash
docker-compose -f ops/compose/docker-compose.dev.yml up --build
```

## Project Structure

```
app/              # Main application code
  api/            # API routes and dependencies
  core/           # Core configuration, security, and logging
  services/       # Business logic services
  db/             # Database models and connections
  workers/        # Background task workers
  cache/          # Caching implementation
  events/         # Event producers and consumers
  utils/          # Utility functions

tests/            # Test suite
ops/              # Operations files (Docker, Kubernetes, CI/CD)
scripts/          # Helper scripts
monitoring/       # Monitoring configurations
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run unit tests:
```bash
pytest tests/unit
```

Run integration tests:
```bash
pytest tests/integration
```

## Deployment

### Docker

Build and run with Docker:
```bash
docker build -t ecommerce-app .
docker run -p 8000:8000 ecommerce-app
```

### Kubernetes

Deploy to Kubernetes:
```bash
kubectl apply -f ops/k8s/
```