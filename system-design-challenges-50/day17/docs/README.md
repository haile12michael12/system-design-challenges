# Day 17 - Eventually Consistent Social Feed

## Challenge Description
Feed updates propagate with delay but high availability. Goal: Demonstrate eventual consistency.

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## System Architecture

This system implements an eventually consistent social feed using the following components:

### Core Components
1. **API Gateway** - FastAPI application handling HTTP requests
2. **Database** - PostgreSQL for persistent storage
3. **Cache** - Redis for caching feeds and posts
4. **Message Broker** - Redis Streams for event propagation
5. **Background Workers** - Celery workers for asynchronous tasks
6. **Monitoring** - Prometheus for metrics collection

### Data Flow
1. User creates a post through the API
2. Post is stored in the database
3. Post creation event is published to Redis Stream
4. Background workers process the event and update follower feeds
5. Updated feeds are cached in Redis
6. Users retrieve their feeds from the cache

## Directory Structure
```
day17/
├── app/                    # Application code
│   ├── core/              # Configuration and core utilities
│   ├── api/               # API routes and endpoints
│   ├── db/                # Database models and repositories
│   ├── domain/            # Domain entities and services
│   ├── cache/             # Cache implementations
│   ├── message_bus/       # Event publishing and consumption
│   ├── workers/           # Background tasks
│   ├── utils/             # Utility functions
│   └── schemas/           # Pydantic models
├── tests/                 # Unit and integration tests
├── infra/                 # Infrastructure configurations
│   ├── docker/            # Dockerfiles
│   ├── compose/           # Docker Compose configurations
│   └── scripts/           # Infrastructure scripts
└── docs/                  # Documentation files
```

## Quickstart

### Prerequisites
- Docker and Docker Compose
- Python 3.8+

### Running the Application

1. **Start all services:**
```bash
cd infra/compose
docker-compose up -d
```

2. **Access the services:**
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Redis Commander: http://localhost:8001

### Development Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Health and Debug
- `GET /debug/health` - Health check
- `GET /debug/metrics-summary` - Metrics summary
- `GET /debug/config` - Current configuration

### Posts
- `POST /posts/` - Create a new post
- `GET /feed/posts/{post_id}` - Get a specific post

### Feed
- `GET /feed/` - Get user's feed

### Users
- `POST /users/` - Create a new user
- `POST /users/{user_id}/follow` - Follow a user
- `POST /users/{user_id}/unfollow` - Unfollow a user

## Monitoring

The system exposes Prometheus metrics at `/metrics` endpoint. Key metrics include:
- HTTP request count and duration
- Database query performance
- Cache hit/miss ratios
- Worker task processing times

## Scaling Considerations

1. **Horizontal Scaling:**
   - API instances can be scaled horizontally behind a load balancer
   - Workers can be scaled based on queue depth
   - Redis can be clustered for high availability

2. **Database Sharding:**
   - Users and posts can be sharded by user ID
   - Each shard can have its own database instance

3. **Caching Strategy:**
   - Hot feeds are cached in Redis
   - Cache expiration is set to balance consistency and performance

## Failure Scenarios

1. **Database Failure:**
   - System becomes read-only
   - Cached data can still be served
   - Write operations queue up for replay

2. **Cache Failure:**
   - All requests go to the database
   - Performance degrades but system remains functional

3. **Worker Backlog:**
   - Feed updates are delayed
   - Eventual consistency window increases
   - Additional workers can be scaled up

## Next Steps

1. Implement more sophisticated feed algorithms
2. Add user authentication and authorization
3. Implement rate limiting and request throttling
4. Add more comprehensive monitoring and alerting
5. Implement data backup and disaster recovery