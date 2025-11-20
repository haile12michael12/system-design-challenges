import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "service" in response.json()