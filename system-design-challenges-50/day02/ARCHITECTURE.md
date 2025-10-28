# Architecture Notes - Day 2 - Weather Dashboard (Non-Functional Requirements Focus)

## System Components

### API Layer
- **FastAPI Service**: Main application server handling HTTP requests
- **Nginx Reverse Proxy**: Load balancing and SSL termination
- **API Gateway**: Rate limiting, authentication, and request routing

### Data Layer
- **PostgreSQL**: Primary database for user data and preferences
- **Redis**: In-memory cache for weather data and session storage
- **Data Replication**: Master-slave replication for read scaling

### Application Layer
- **Business Logic**: Services layer implementing weather data processing
- **Background Workers**: Asynchronous tasks for data fetching and processing
- **Caching Layer**: Multi-level caching strategy (API-level and database-level)

### Monitoring & Observability
- **Metrics Collection**: Custom metrics collector tracking response times, error rates
- **Health Checks**: Component-level health monitoring
- **Logging**: Structured logging for debugging and auditing
- **Alerting**: Notification system for system issues

### Infrastructure
- **Containerization**: Docker for consistent deployment environments
- **Orchestration**: Docker Compose for multi-container applications
- **Auto-scaling**: Horizontal pod autoscaler based on CPU and memory usage

## Suggested Non-Functional Requirements
- **Target users / TPS**: 1M daily active users, 10,000 requests per second peak
- **Latency targets**: 95th percentile response time < 200ms
- **Availability SLA**: 99.99% uptime
- **Data durability requirements**: All user data persisted with backups
- **Security considerations**: HTTPS, input validation, secure headers

## Failure Scenarios to Consider
- **DB partition**: Implement database sharding and failover
- **Cache failure**: Graceful degradation to database queries
- **Worker backlog**: Auto-scaling for worker processes
- **Network latency**: CDN for static assets, geo-distributed services
- **Service degradation**: Circuit breaker pattern for external dependencies

## Scalability Considerations
- **Horizontal vs vertical scaling**: Horizontal scaling for stateless services
- **Database sharding strategy**: Shard by geographic region
- **Caching strategy**: Multi-level caching with Redis
- **Load balancing approach**: Round-robin with health checks
- **CDN requirements**: Static asset delivery for global users

## Technology Choices
- **Database choice**: PostgreSQL for ACID compliance and relational data
- **Caching strategy**: Redis for in-memory caching with TTL
- **Queueing mechanism**: Redis Streams for lightweight messaging
- **Monitoring approach**: Custom metrics collector with health endpoints

## Deployment Architecture
```
Internet -> Load Balancer -> Nginx -> FastAPI App -> PostgreSQL/Redis
                    ↓
              Background Workers
```

## Data Flow
1. User requests weather data through API
2. Check Redis cache for existing data
3. If not in cache, fetch from external weather API
4. Store in cache with TTL
5. Return data to user
6. Background workers periodically update cache

## Performance Optimization
- Connection pooling for database connections
- Async I/O for non-blocking operations
- Response compression for large payloads
- Database indexing for common queries
