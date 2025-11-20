# Architecture Documentation - Day 11: Auto-Scaler Visualizer

## Overview
The Auto-Scaler Visualizer is a system designed to simulate and visualize the behavior of vertical vs horizontal scaling strategies. It helps users understand when to scale up/out based on cost and latency trade-offs.

## System Components

### Backend (FastAPI)
- **API Layer**: Exposes REST endpoints for health checks, simulation control, and autoscaling recommendations
- **Business Logic**: Implements scaling algorithms and simulation logic
- **Data Layer**: Manages database connections and data models
- **Worker Layer**: Handles background processing with Celery

### Frontend (React/Vite)
- **Visualization**: Interactive charts showing latency vs cost trade-offs
- **Controls**: UI for configuring simulations and scaling parameters
- **Dashboard**: Real-time display of simulation results

### Infrastructure
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for session storage and message brokering
- **Worker Queue**: Celery with Redis backend
- **Reverse Proxy**: Nginx for load balancing and SSL termination

## Data Flow
1. User configures simulation parameters via frontend
2. Frontend sends request to backend API
3. Backend queues simulation task to Celery worker
4. Worker processes simulation and stores results in database
5. Frontend polls for results and visualizes data

## Scaling Strategies
- **Vertical Scaling**: Increase resources of existing instances
- **Horizontal Scaling**: Add more instances to distribute load

## Deployment Options
- Docker Compose for local development
- Kubernetes for production deployments
- Terraform for cloud infrastructure provisioning