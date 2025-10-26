# Architecture Notes - Day 18 - Latency-Aware News App

## Components to Consider
- API Gateway / Load Balancer
- FastAPI service(s)
- Postgres (or compatible) storage
- Cache (Redis)
- Worker queue (RabbitMQ / Redis Streams)
- Monitoring and logging stack

## Suggested Non-Functional Requirements
- Target users / TPS:
- Latency targets:
- Availability SLA:
- Data durability requirements:
- Security considerations:

## Failure Scenarios to Consider
- DB partition
- Cache failure
- Worker backlog
- Network latency
- Service degradation

## Scalability Considerations
- Horizontal vs vertical scaling
- Database sharding strategy
- Caching strategy
- Load balancing approach
- CDN requirements

## Technology Choices
- Justify your choice of database (SQL vs NoSQL)
- Explain caching strategy
- Describe queueing mechanism
- Outline monitoring approach
