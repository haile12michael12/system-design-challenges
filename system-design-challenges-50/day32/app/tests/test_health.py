import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Test the health check endpoint
    """
    response = client.get("/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert data["status"] == "healthy"
    assert data["service"] == "document-editor"

def test_root_endpoint():
    """
    Test the root endpoint
    """
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data