# Day 13 - Payment Processing Service

## Challenge Description
Build a payment processing service with retry logic, idempotency, and monitoring.

## Project Structure
```
day13/
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── config.py
│ ├── prometheus_middleware.py
│ ├── db/
│ │ ├── __init__.py
│ │ ├── database.py
│ │ └── models.py
│ ├── routes/
│ │ ├── __init__.py
│ │ └── payments.py
│ ├── services/
│ │ └── payment_processor.py
│ ├── workers/
│ │ └── worker.py
│ └── utils/
│ └── logger.py
├── tests/
│ ├── __init__.py
│ └── test_integration.py
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── ARCHITECTURE.md
```

## Quickstart

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose
```bash
docker-compose up --build
```

### Running Locally
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Payments
- `POST /api/v1/payments` - Process a payment
- `GET /api/v1/payments/{payment_id}` - Get payment status

## Testing
```bash
pytest tests/
```