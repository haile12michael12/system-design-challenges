# Day 48 - Data Lake Ingestion Framework

## Overview
A comprehensive data lake ingestion framework designed for large-scale data processing with schema evolution and partitioning capabilities. This system provides a robust foundation for ingesting, processing, and managing data in a data lake environment.

## Features

### Core Capabilities
- **Data Ingestion**: Batch processing with configurable job scheduling
- **Schema Evolution**: Versioned schema management with backward compatibility
- **Partitioning**: Multiple partitioning strategies (date, hash, range, list)
- **Storage Abstraction**: S3-compatible storage with MinIO support
- **Background Processing**: Asynchronous job processing with workers
- **RESTful API**: Comprehensive API for all operations

### Advanced Features
- **Partition Optimization**: Automatic merging of small partitions
- **Schema Comparison**: Diff-based schema change detection
- **Job Management**: Full lifecycle management of ingestion jobs
- **Monitoring**: Health checks and comprehensive logging
- **Scalability**: Horizontal scaling with load balancing

## Architecture

The system follows a microservices architecture with the following components:

- **API Layer**: FastAPI application with Nginx load balancer
- **Data Processing**: Services for ingestion, schema management, and partitioning
- **Storage**: PostgreSQL for metadata, Redis for caching, S3-compatible for data
- **Workers**: Background processes for job execution

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   cd day48
   ```

2. **Start all services**:
   ```bash
   make start
   # or manually:
   # docker-compose up -d
   ```

3. **Access the services**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001 (minioadmin/minioadmin123)

### Local Development

1. **Install dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Start the API server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. **Start the worker** (in another terminal):
   ```bash
   python -m app.workers.main
   ```

## API Usage

### Create a Data Lake Table
```bash
curl -X POST "http://localhost:8000/api/v1/tables/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "user_events",
    "description": "User interaction events",
    "partition_strategy": "date",
    "partition_columns": ["year", "month", "day"],
    "storage_format": "parquet",
    "compression": "snappy"
  }'
```

### Create an Ingestion Job
```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "daily_user_events",
    "data_source_id": 1,
    "table_id": 1,
    "batch_size": 10000,
    "priority": 5
  }'
```

### Start a Job
```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/jobs/1/start"
```

### Create a Schema Version
```bash
curl -X POST "http://localhost:8000/api/v1/schema/versions" \
  -H "Content-Type: application/json" \
  -d '{
    "table_id": 1,
    "schema_definition": {
      "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "event_type", "type": "string"},
        {"name": "timestamp", "type": "long"},
        {"name": "properties", "type": "map", "values": "string"}
      ]
    },
    "description": "Initial schema for user events"
  }'
```

## Available Commands

Use the Makefile for common operations:

```bash
# Development
make dev              # Start development server
make install          # Install dependencies

# Docker
make build            # Build Docker images
make up               # Start all services
make down             # Stop all services
make logs             # Show logs

# Testing
make test             # Run all tests
make test-unit        # Run unit tests
make test-integration # Run integration tests

# Code Quality
make lint             # Run linting
make format           # Format code

# Database
make db-init          # Initialize database
make db-reset         # Reset database (WARNING: deletes data)

# Monitoring
make status           # Show service status
make health           # Check API health
```

## Configuration

The application uses environment variables for configuration. See `app/config/settings.py` for all available options.

### Key Configuration Options

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/datalake

# Redis
REDIS_URL=redis://localhost:6379/0

# Storage
STORAGE_BUCKET=datalake-storage
STORAGE_ENDPOINT=http://localhost:9000
STORAGE_REGION=us-east-1

# AWS Credentials (for S3/MinIO)
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin123
```

## Testing

The project includes comprehensive tests:

- **Unit Tests**: Test individual components and utilities
- **Integration Tests**: Test API endpoints and database interactions

Run tests:
```bash
# All tests
make test

# With coverage
make test-coverage

# Specific test type
make test-unit
make test-integration
```

## Development

### Project Structure
```
app/
├── api/              # API endpoints
├── config/           # Configuration and database setup
├── models/           # Database models
├── services/         # Business logic services
├── utils/            # Utility functions
├── workers/          # Background workers
└── main.py          # FastAPI application

tests/
├── unit/            # Unit tests
└── integration/     # Integration tests
```

### Adding New Features

1. **Database Models**: Add to `app/models/`
2. **Business Logic**: Add to `app/services/`
3. **API Endpoints**: Add to `app/api/`
4. **Background Jobs**: Add to `app/workers/`

### Code Quality

The project enforces code quality through:
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing

Run quality checks:
```bash
make lint
make format
```

## Production Deployment

### Docker Compose
The included `docker-compose.yml` is suitable for development and small-scale production.

### Kubernetes
For production at scale, deploy to Kubernetes with:
- Managed PostgreSQL (AWS RDS, Google Cloud SQL)
- Managed Redis (AWS ElastiCache, Google Memorystore)
- S3 or Google Cloud Storage for data lake

### Environment Variables
Set production environment variables:
```bash
DATABASE_URL=postgresql://user:pass@prod-db:5432/datalake
REDIS_URL=redis://prod-redis:6379/0
STORAGE_BUCKET=prod-datalake
STORAGE_ENDPOINT=https://s3.amazonaws.com
```

## Monitoring

### Health Checks
- API Health: `GET /health`
- Service Status: `make status`

### Logging
Structured logging with configurable levels:
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARN, ERROR, CRITICAL
```

### Metrics
The system exposes metrics for:
- Job success/failure rates
- Processing times
- Data volume processed
- System resource usage

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running: `docker-compose ps`
   - Verify connection string in environment variables

2. **Redis Connection Failed**
   - Check Redis is running: `docker-compose ps`
   - Verify Redis URL configuration

3. **Storage Access Denied**
   - Check MinIO/S3 credentials
   - Verify bucket exists and is accessible

4. **Worker Not Processing Jobs**
   - Check worker logs: `make logs-worker`
   - Verify Redis connection
   - Check job status in database

### Debug Mode
Enable debug logging:
```bash
LOG_LEVEL=DEBUG make dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run quality checks: `make lint && make test`
6. Submit a pull request

## License

This project is part of the System Design Challenges series.
