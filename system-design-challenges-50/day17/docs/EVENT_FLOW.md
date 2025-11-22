# Event Flow in the Social Feed System

## Overview

This document describes the event flow architecture in the social feed system, detailing how events are generated, propagated, and processed throughout the system.

## Event-Driven Architecture

The system uses an event-driven architecture to achieve loose coupling between components and enable asynchronous processing. Events are used to propagate changes and trigger actions across the system.

## Core Events

### 1. PostCreatedEvent

#### Trigger
When a user creates a new post through the API.

#### Data
- `post_id`: Unique identifier for the post
- `user_id`: ID of the user who created the post
- `content`: Content of the post
- `timestamp`: Time of creation

#### Flow
1. User creates post via API
2. Post is stored in database
3. PostCreatedEvent is published to Redis Stream
4. Workers consume event and update follower feeds
5. Updated feeds are cached

### 2. FollowerAddedEvent

#### Trigger
When a user follows another user.

#### Data
- `follower_id`: ID of the user who initiated the follow
- `followed_id`: ID of the user being followed
- `timestamp`: Time of follow action

#### Flow
1. User follows another user via API
2. Follow relationship is stored in database
3. FollowerAddedEvent is published to Redis Stream
4. Workers consume event and initialize feed propagation
5. Existing posts from followed user are propagated to follower

### 3. PostLikedEvent

#### Trigger
When a user likes a post.

#### Data
- `post_id`: ID of the post being liked
- `user_id`: ID of the user who liked the post
- `timestamp`: Time of like action

#### Flow
1. User likes post via API
2. Like is stored in database
3. PostLikedEvent is published to Redis Stream
4. Workers consume event and update engagement metrics
5. Engagement data is used for feed ranking

## Event Publishing

### Publisher Component
The `EventPublisher` class is responsible for publishing events to the message bus.

### Implementation
```python
class EventPublisher:
    def publish(self, event: EventSchema) -> bool:
        # Convert event to JSON
        event_json = json.dumps(event.dict())
        
        # Publish to Redis stream
        stream_name = f"events:{event.event_type}"
        self.redis_client.client.xadd(stream_name, {"data": event_json})
```

### Publishing Strategies
1. **Synchronous Publishing**: Events published immediately after database commit
2. **Batch Publishing**: Events queued and published in batches for efficiency
3. **Reliable Publishing**: With retry mechanisms for failed publications

## Event Consumption

### Consumer Component
The `EventConsumer` class consumes events from the message bus and routes them to appropriate handlers.

### Implementation
```python
class EventConsumer:
    def register_handler(self, event_type: str, handler: Callable) -> None:
        self.handlers[event_type] = handler
    
    async def consume_from_stream(self, stream_name: str) -> None:
        while True:
            # Read events from stream
            response = self.redis_client.client.xread(
                {stream_name: last_id}, 
                count=1, 
                block=1000
            )
            
            if response:
                # Process the event
                await self._process_event(message_data)
```

### Consumption Patterns
1. **Single Consumer**: One worker processes all events of a type
2. **Competing Consumers**: Multiple workers process events in parallel
3. **Routing**: Events routed to specific consumers based on content

## Event Processing

### Worker Tasks
Celery workers process events through dedicated tasks:

1. **Feed Propagation Task**: Updates follower feeds when new posts are created
2. **Cache Invalidation Task**: Invalidates caches when data changes
3. **Metrics Reporting Task**: Collects and reports system metrics

### Processing Guarantees
1. **At-Least-Once**: Events may be processed multiple times
2. **Idempotency**: Processing the same event multiple times has the same effect
3. **Ordering**: Events processed in order within a stream

## Event Storage

### Redis Streams
Events are stored in Redis Streams, which provide:
- Persistent storage with configurable retention
- Consumer group support for parallel processing
- Acknowledgment mechanism for reliability

### Stream Organization
- `events:post_created` - Post creation events
- `events:follower_added` - User follow events
- `events:post_liked` - Post like events

## Error Handling

### Publication Errors
1. **Retry Logic**: Failed publications retried with exponential backoff
2. **Dead Letter Queue**: Unprocessable events moved to separate queue
3. **Alerting**: Critical publication failures trigger alerts

### Consumption Errors
1. **Message Nack**: Failed messages are requeued
2. **Circuit Breaker**: Prevents cascade failures
3. **Error Logging**: Detailed error information for debugging

## Monitoring

### Event Metrics
1. **Event Volume**: Number of events published per second
2. **Processing Latency**: Time from event publication to processing
3. **Error Rate**: Percentage of failed event processing
4. **Backlog**: Number of unprocessed events

### Health Checks
1. **Publisher Health**: Verify ability to publish events
2. **Consumer Health**: Verify ability to consume events
3. **Stream Health**: Check Redis Stream status and performance

## Scalability

### Horizontal Scaling
1. **Multiple Publishers**: API instances can publish events concurrently
2. **Multiple Consumers**: Workers can consume events in parallel
3. **Stream Sharding**: High-volume event types can use multiple streams

### Performance Optimization
1. **Batch Processing**: Process multiple events in single database transactions
2. **Asynchronous I/O**: Non-blocking operations for better throughput
3. **Connection Pooling**: Efficient use of database and Redis connections

## Security

### Event Validation
1. **Schema Validation**: Events validated against defined schemas
2. **Authentication**: Publishers authenticated before publishing
3. **Authorization**: Access control for event types

### Data Protection
1. **Encryption**: Sensitive data encrypted in events
2. **Audit Logging**: All event publications and consumptions logged
3. **Data Retention**: Events automatically deleted after retention period

## Best Practices

### 1. Event Design
- Keep events small and focused
- Use versioning for event schemas
- Include all necessary data for processing

### 2. Idempotency
- Design event processing to be idempotent
- Use unique event identifiers
- Track processed events to prevent duplicates

### 3. Error Handling
- Implement comprehensive error handling
- Log errors with sufficient context
- Implement circuit breakers for external dependencies

### 4. Monitoring
- Monitor event flow end-to-end
- Set up alerts for anomalies
- Track business metrics derived from events

## Future Improvements

### 1. Event Sourcing
- Store all events as source of truth
- Rebuild state from event history
- Enable time-travel debugging

### 2. Complex Event Processing
- Detect patterns across multiple events
- Trigger actions based on event correlations
- Implement real-time analytics

### 3. Event Streaming Platforms
- Migrate to dedicated streaming platforms (Kafka, RabbitMQ)
- Leverage advanced streaming features
- Improve scalability and reliability

## Troubleshooting

### Common Issues
1. **Event Processing Delays**: Check worker capacity and database performance
2. **Duplicate Events**: Verify idempotency implementation
3. **Lost Events**: Check Redis Stream configuration and retention policies

### Diagnostic Tools
1. **Event Tracing**: Track events through the system
2. **Metrics Dashboard**: Visualize event flow and performance
3. **Log Aggregation**: Centralized logging for error analysis