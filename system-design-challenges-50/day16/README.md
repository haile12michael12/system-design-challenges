# Authentication Service

## Overview
A strongly consistent authentication microservice with immediate consistency after password resets. This service provides user registration, login, token management, and password reset functionality.

## Features
- User registration and authentication
- JWT-based token management
- Password reset functionality
- Email notifications
- Rate limiting
- Token blacklisting
- Background task processing
- Strong consistency guarantees

## Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Redis
- Node.js (for frontend)

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (copy `.env` from `.env.example` and modify as needed)

### Running the Application

#### Backend
```bash
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### With Docker Compose
```bash
cd infrastructure/docker
docker-compose up --build
```

## Project Structure

```
app/              # Backend (FastAPI)
  core/           # Core configuration and security
  db/             # Database models and sessions
  routes/         # API routes
  schemas/        # Pydantic schemas
  services/       # Business logic services
  utils/          # Utility functions
  workers/        # Background workers

frontend/         # Frontend (React/Vite)
infrastructure/   # Docker and Nginx configuration
scripts/          # Utility scripts
tests/            # Test suite
config/           # Configuration files
resources/        # Templates and resources
```

## API Documentation
Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run unit tests:
```bash
pytest tests/unit
```

Run integration tests:
```bash
pytest tests/integration
```

## Deployment

### Docker
Build and run with Docker:
```bash
docker build -t auth-service .
docker run -p 8000:8000 auth-service
```

### Docker Compose
Deploy with Docker Compose:
```bash
cd infrastructure/docker
docker-compose up -d
```
