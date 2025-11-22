# Architecture Notes - Day 17 - Eventually Consistent Social Feed

## System Overview

This system implements an eventually consistent social feed, where updates to user feeds may take some time to propagate but the system remains highly available. The architecture is designed to handle high throughput with eventual consistency as a trade-off for availability and performance.

## Components

### 1. API Gateway (FastAPI)
- Handles HTTP requests and responses
- Implements RESTful endpoints for posts, feeds, and users
- Provides health checks and metrics endpoints
- Handles request validation and serialization

### 2. Domain Layer
- **Entities**: Post, User, Feed
- **Services**: FeedWriterService, FeedReaderService
- **Events**: PostCreatedEvent, FollowerAddedEvent

### 3. Data Layer
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Repositories**: PostRepository, UserRepository, FollowerRepository
- **Models**: Post, User, Follow, Like

### 4. Caching Layer
- **Redis**: Used for caching feeds and individual posts
- **PostCache**: Caches individual posts
- **FeedCache**: Caches user feeds

### 5. Message Bus
- **Redis Streams**: Used for event propagation
- **EventPublisher**: Publishes domain events
- **EventConsumer**: Consumes and processes events

### 6. Background Workers
- **Celery**: Asynchronous task processing
- **Feed Propagation**: Updates follower feeds when new posts are created
- **Cache Invalidation**: Invalidates caches when data changes
- **Metrics Reporting**: Collects and reports system metrics

### 7. Monitoring
- **Prometheus**: Metrics collection and storage
- **Custom Metrics**: HTTP requests, cache performance, worker stats

## Data Flow

### Post Creation Flow
1. User sends POST request to create a post
2. API validates request and forwards to FeedWriterService
3. FeedWriterService stores post in database
4. PostCreatedEvent is published to Redis Stream
5. Worker consumes event and updates follower feeds
6. Updated feeds are cached in Redis

### Feed Retrieval Flow
1. User requests their feed
2. System first checks Redis cache
3. If cache miss, retrieves posts from database
4. Feed is cached in Redis for future requests
5. Feed is returned to user

### User Following Flow
1. User sends request to follow another user
2. API validates request and forwards to FeedWriterService
3. FeedWriterService updates follow relationship in database
4. FollowerAddedEvent is published to Redis Stream
5. Worker consumes event and initializes feed propagation

## Consistency Model

This system uses eventual consistency with the following characteristics:

### Consistency Guarantees
- **Strong Consistency**: User's own posts are immediately visible
- **Eventual Consistency**: Follower feeds are updated asynchronously
- **Convergence**: All followers will eventually see new posts

### Consistency Windows
- **Typical**: < 1 second for feed updates
- **Degraded**: Up to several seconds during high load
- **Failure**: Up to minutes during system failures

## Scalability Patterns

### Horizontal Scaling
- **API Instances**: Multiple FastAPI instances behind load balancer
- **Workers**: Multiple Celery workers processing different queues
- **Database**: Read replicas for scaling read operations

### Database Sharding
- **Sharding Key**: User ID
- **Shard Distribution**: Consistent hashing for even distribution
- **Cross-Shard Queries**: Minimized through data denormalization

### Caching Strategy
- **Hot Data**: Frequently accessed feeds cached in Redis
- **Cache Expiration**: TTL-based expiration to balance consistency
- **Cache Warming**: Proactive caching of popular feeds

## Failure Handling

### Database Failures
- **Read Failures**: Fallback to cache or degraded mode
- **Write Failures**: Queue operations for replay
- **Connection Failures**: Retry with exponential backoff

### Cache Failures
- **Cache Miss**: Direct database access
- **Cache Server Down**: Graceful degradation
- **Cache Inconsistency**: Cache invalidation strategies

### Worker Failures
- **Task Failures**: Retry mechanisms with backoff
- **Worker Crashes**: Automatic restart by process manager
- **Queue Backlog**: Auto-scaling of worker instances

## Monitoring and Observability

### Metrics Collection
- **Application Metrics**: Request rates, error rates, latency
- **System Metrics**: CPU, memory, disk usage
- **Business Metrics**: Posts created, follows, feed updates

### Health Checks
- **Liveness**: Basic process health
- **Readiness**: Dependencies availability
- **Deep**: End-to-end functionality verification

### Alerting
- **Critical**: System unavailable, data loss
- **Warning**: Performance degradation, high error rates
- **Info**: Scaling events, routine maintenance

## Security Considerations

### Authentication
- **JWT Tokens**: For API authentication
- **Token Expiration**: Configurable expiration times
- **Refresh Tokens**: For extended sessions

### Authorization
- **Role-Based Access**: Different permissions for users
- **Resource Ownership**: Users can only modify their own data
- **Rate Limiting**: Prevent abuse and DoS attacks

### Data Protection
- **Encryption**: At rest and in transit
- **Input Validation**: Prevent injection attacks
- **Audit Logging**: Track sensitive operations

## Performance Optimization

### Database Optimization
- **Indexes**: On frequently queried columns
- **Connection Pooling**: Efficient database connection usage
- **Query Optimization**: Minimize complex joins

### Caching Optimization
- **Cache Keys**: Efficient key design for fast lookups
- **Cache Size**: Memory management and eviction policies
- **Cache Pre-warming**: Load frequently accessed data

### Network Optimization
- **Compression**: HTTP response compression
- **CDN**: For static assets
- **Connection Reuse**: HTTP keep-alive and connection pooling

## Trade-offs and Design Decisions

### Consistency vs Availability
- **Chosen**: High availability with eventual consistency
- **Rationale**: Better user experience and system resilience
- **Impact**: Users may see slightly stale data

### Simplicity vs Functionality
- **Chosen**: Simple design with core functionality
- **Rationale**: Easier to understand and maintain
- **Impact**: Advanced features deferred to future iterations

### Performance vs Resource Usage
- **Chosen**: Optimized for performance within resource constraints
- **Rationale**: Cost-effective scaling
- **Impact**: May require more sophisticated tuning for extreme loads