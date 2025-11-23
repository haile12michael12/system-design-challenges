# Event-Driven Order Processing System

An event-driven order processing system that demonstrates asynchronous processing patterns using RabbitMQ, Celery, and microservices architecture.

## Features

- Event-driven architecture with RabbitMQ message broker
- Asynchronous task processing with Celery workers
- RESTful API for order management
- PostgreSQL for persistent storage
- Redis for caching and task results
- Docker containerization for easy deployment

## Architecture

![Architecture Diagram](docs/architecture.png)

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Start services: `docker-compose up`

## API Endpoints

- `POST /orders/` - Create a new order
- `GET /orders/{id}` - Get order by ID
- `GET /orders/` - List all orders
- `GET /health` - Health check

## Services

- **API Service**: FastAPI application for handling HTTP requests
- **Worker Service**: Celery workers for background task processing
- **Database**: PostgreSQL for data persistence
- **Cache**: Redis for caching and task results
- **Message Broker**: RabbitMQ for event streaming

## Testing

Run tests with:
```bash
pytest tests/
```

## Monitoring

- RabbitMQ Management Console: http://localhost:15672
- API Documentation: http://localhost:8000/docs