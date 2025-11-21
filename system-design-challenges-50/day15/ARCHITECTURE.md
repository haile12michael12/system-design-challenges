# Post Service Architecture

## Overview
This document describes the architecture of the Post Service, a social media platform for creating and sharing posts.

## System Components

### API Layer
- **FastAPI Service**: Main application service handling HTTP requests
- **Routes**: REST API endpoints for posts and health checks
- **Schemas**: Data validation and serialization

### Domain Layer
- **Entities**: Core business entities (Post)
- **Value Objects**: Immutable value objects (PostId)
- **Events**: Domain events (PostCreated)

### Application Layer
- **Commands**: Write operations (CreatePost)
- **Queries**: Read operations (GetPost, FeedQuery)
- **Handlers**: Command and query handlers
- **DTOs**: Data transfer objects

### Infrastructure Layer
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for caching
- **Messaging**: Internal message broker for event handling
- **Instrumentation**: Prometheus metrics and OpenTelemetry tracing

### Workers
- **Celery**: Background task processing
- **Tasks**: Event handling tasks

## Technology Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Messaging**: Internal message broker
- **Workers**: Celery
- **Monitoring**: Prometheus, OpenTelemetry
- **Containerization**: Docker

## Deployment
- **Docker Compose**: Multi-container deployment
- **Services**: App, Worker, Redis, PostgreSQL
