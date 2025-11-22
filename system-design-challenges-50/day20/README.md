# Day 20: Cost Optimization Recommendation Engine

A cost optimization recommendation engine with SLA validation, simulation capabilities, and automated cost management.

## Features

- **Cost Optimization Recommendations**: Generate actionable recommendations to reduce cloud costs
- **SLA Validation**: Ensure recommendations don't violate service level agreements
- **Cost Simulation**: Simulate cost impact of proposed changes before implementation
- **Automated Cost Management**: Background workers for cost recomputation and budget monitoring
- **Metrics Integration**: Connect to telemetry systems for performance data
- **Billing Integration**: Connect to billing systems for cost data
- **Containerization**: Docker and Docker Compose for easy deployment

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Recommend  │  │   Metrics   │  │      Config Apply       │ │
│  │   Routes    │  │   Routes    │  │        Routes           │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     Simulate Routes                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ▲              ▲              ▲              ▲
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Cost Model      │ │ SLA Engine      │ │ Billing         │ │ Telemetry       │
│ Service         │ │ Service         │ │ Connector       │ │ Connector       │
│                 │ │                 │ │ Service         │ │ Service         │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
         ▲              ▲              ▲              ▲
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Simulation Engine                        │
│                        Service                                  │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Database Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Services   │  │  Recommen-  │  │     Config              │  │
│  │    ORM      │  │   dations   │  │    Changes              │  │
│  │             │  │             │  │                         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Simulations                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Background Workers                      │
│  ┌─────────────┐  ┌──────────────────────────────────────────┐  │
│  │   Costs     │  │              Metrics                     │  │
│  │  Recompute  │  │              Pull                        │  │
│  └─────────────┘  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### API Routes (v1)
- `recommend.py`: Cost optimization recommendations
- `metrics.py`: Metrics querying and monitoring
- `config_apply.py`: Apply/rollback recommendations
- `simulate.py`: Cost impact simulations

### Core Modules
- `config.py`: Application settings and environment loading
- `security.py`: Security utilities and authentication
- `observability.py`: Metrics and logging setup

### Database
- `models.py`: ORM models for services, recommendations, simulations, config changes
- `session.py`: Database session management
- `repositories/`: CRUD operations for each model

### Services
- `cost_model.py`: Cost optimization modeling and recommendations
- `sla_engine.py`: SLA compliance validation and monitoring
- `billing_connector.py`: Billing system integration
- `telemetry_connector.py`: Telemetry system integration
- `simulation_engine.py`: Cost optimization simulations

### Workers
- `celery_app.py`: Celery application configuration
- `tasks/recompute_costs.py`: Cost recomputation and budget monitoring
- `tasks/pull_metrics.py`: Metrics collection and analysis

### Schemas
- `recommendation.py`: Recommendation and simulation data models
- `metrics.py`: Metrics data models
- `common.py`: Common data models

### Utilities
- `logging.py`: Structured logging utilities
- `cache.py`: Redis caching utilities
- `validators.py`: Input validation utilities

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.9+

### Running with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start required services (PostgreSQL and Redis)
# You can use Docker for this:
docker-compose up -d db redis

# Start the API server
python app/main.py

# In another terminal, start the Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# In another terminal, start the Celery beat scheduler
celery -A app.workers.celery_app beat --loglevel=info
```

## API Endpoints

### Recommendations
- `POST /v1/recommend` - Generate cost optimization recommendations
- `GET /v1/recommendations/{service_id}` - Get historical recommendations

### Metrics
- `POST /v1/metrics/query` - Query service metrics
- `GET /v1/metrics/services` - List monitored services
- `GET /v1/metrics/{service_id}/health` - Get service health status

### Configuration
- `POST /v1/config/apply` - Apply a recommendation
- `POST /v1/config/rollback/{service_id}/{recommendation_id}` - Rollback a recommendation
- `GET /v1/config/history/{service_id}` - Get configuration change history

### Simulation
- `POST /v1/simulate` - Run a cost optimization simulation
- `GET /v1/simulate/templates` - Get available simulation templates
- `POST /v1/simulate/batch` - Run multiple simulations in batch

## Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_cost_model.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://postgres:password@localhost:5432/cost_optimizer` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `DEBUG` | Debug mode | `False` |
| `PROMETHEUS_URL` | Prometheus URL | `http://localhost:9090` |
| `GRAFANA_URL` | Grafana URL | `http://localhost:3000` |
| `BILLING_API_URL` | Billing API URL | `http://billing-service:8000` |
| `BILLING_API_KEY` | Billing API key | `secret-key` |

## Project Structure

```
day20/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── recommend.py
│   │       ├── metrics.py
│   │       ├── config_apply.py
│   │       └── simulate.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── observability.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── session.py
│   │   └── repositories/
│   │       └── recommendation_repo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cost_model.py
│   │   ├── sla_engine.py
│   │   ├── billing_connector.py
│   │   ├── telemetry_connector.py
│   │   └── simulation_engine.py
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   └── tasks/
│   │       ├── __init__.py
│   │       ├── recompute_costs.py
│   │       └── pull_metrics.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── recommendation.py
│   │   ├── metrics.py
│   │   └── common.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       ├── cache.py
│       └── validators.py
├── tests/
│   ├── unit/
│   │   ├── test_cost_model.py
│   │   ├── test_sla_engine.py
│   │   └── test_recommendation_api.py
│   └── integration/
│       ├── test_db_integration.py
│       └── test_worker_pipeline.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```