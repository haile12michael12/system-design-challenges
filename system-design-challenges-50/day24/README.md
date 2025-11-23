# Failover Dashboard

A real-time dashboard for monitoring and managing database replication failover across multiple regions.

## Features

- Real-time monitoring of database replica status across regions
- Visualization of replication lag metrics
- Simulate replication lag and outages for testing
- Automated failover orchestration
- WebSocket-based real-time updates
- Historical data tracking and visualization

## Architecture

![Architecture Diagram](docs/architecture.png)

## Getting Started

1. Clone the repository
2. Set up environment variables in `.env`
3. Start services: `docker-compose up`

## Services

- **API Service**: FastAPI backend with REST and WebSocket endpoints
- **Frontend**: Next.js 14 dashboard with real-time updates
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for state management and messaging
- **Workers**: Celery workers for background tasks

## API Endpoints

- `GET /health` - Health check
- `POST /simulate/lag` - Simulate replication lag
- `POST /simulate/outage` - Simulate region outage
- `WebSocket /ws/regions` - Real-time region status updates

## Development

### Backend
```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```