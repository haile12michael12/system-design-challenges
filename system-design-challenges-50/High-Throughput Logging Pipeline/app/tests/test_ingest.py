import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.logs import LogIn, LogLevel
from datetime import datetime

client = TestClient(app)

def test_ingest_single_log():
    """
    Test ingesting a single log entry
    """
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO",
        "message": "Test log message",
        "service": "test-service"
    }
    
    response = client.post(
        "/ingest/",
        json=log_data,
        headers={"x-api-key": "test-api-key"}
    )
    # We expect this to return 404 because the endpoint is not implemented yet
    assert response.status_code == 404

def test_ingest_batch_logs():
    """
    Test ingesting a batch of log entries
    """
    batch_data = {
        "logs": [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "INFO",
                "message": "Test log message 1",
                "service": "test-service"
            },
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "ERROR",
                "message": "Test log message 2",
                "service": "test-service"
            }
        ]
    }
    
    response = client.post(
        "/ingest/batch",
        json=batch_data,
        headers={"x-api-key": "test-api-key"}
    )
    # We expect this to return 404 because the endpoint is not implemented yet
    assert response.status_code == 404

def test_ingest_without_api_key():
    """
    Test ingesting a log without API key
    """
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO",
        "message": "Test log message",
        "service": "test-service"
    }
    
    response = client.post("/ingest/", json=log_data)
    assert response.status_code == 422  # Validation error for missing header