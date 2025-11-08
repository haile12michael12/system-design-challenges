# System Design Coach App - Architecture

## Overview

The System Design Coach App is a platform for learning and practicing system design skills. Users can work on system design challenges, submit their solutions with diagrams and explanations, and receive automated feedback.

## Architecture Components

### 1. API Layer
- **FastAPI** framework for RESTful API endpoints
- **Pydantic** models for request/response validation
- **Custom error handlers** for consistent error responses

### 2. Data Layer
- **SQLAlchemy** ORM for database interactions
- **PostgreSQL** as the primary database
- **Alembic** for database migrations
- **Async database sessions** for improved performance

### 3. Business Logic Layer
- **Service modules** for each entity (users, prompts, submissions, gradings)
- **Separation of concerns** with distinct modules for different functionalities

### 4. Background Processing
- **Celery** for asynchronous task processing
- **Redis** as the message broker
- **Task queues** for grading and notifications

### 5. External Integrations
- **AWS S3** for storing diagram files
- **AI/ML models** for automated grading
- **Prometheus** for metrics collection
- **Sentry** for error tracking

### 6. Utilities
- **File handling** utilities for secure file operations
- **Validation** utilities for input sanitization
- **Time formatting** utilities for consistent time handling

## Data Flow

1. User submits a system design solution (diagram + explanation)
2. Solution is stored in the database
3. Background task is queued for AI grading
4. AI grading service evaluates the solution
5. Grading results are stored in the database
6. Notification is sent to the user

## Deployment

- **Docker** containers for consistent deployment
- **Docker Compose** for multi-service orchestration
- **Environment variables** for configuration management