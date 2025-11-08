# System Design Coach App

## Challenge Description
A platform that asks system design questions and grades your diagrams + trade-off explanations. Goal: Meta-project to master interviews.

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a comprehensive prototype using FastAPI and Postgres-compatible patterns
- Add monitoring, background processing, and AI grading capabilities

## Project Structure
```
app/
├── schemas/          # Pydantic models for request/response
├── db/               # Database layer with SQLAlchemy models
├── services/         # Business logic layer
├── workers/          # Background tasks and queues
├── integrations/     # External integrations (S3, AI models, monitoring)
├── utils/            # Shared utilities
├── errors.py         # Custom error handlers
└── main.py           # FastAPI application entry point

scripts/              # CLI tools, db init, linting, seeding
docs/                 # Documentation
```

## Quickstart
```bash
# Clone the repository
git clone <repository-url>
cd system-design-coach-app

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Run the application
uvicorn app.main:app --reload --port 8000
```

## Docker Quickstart
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Linting
```bash
# Run linting scripts
./scripts/lint.sh
```

### Database Migrations
```bash
# Initialize migrations
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Environment Variables
Copy `.env.example` to `.env` and update the values as needed.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Design Decisions](docs/DESIGN_DECISIONS.md)
