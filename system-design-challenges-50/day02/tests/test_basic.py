import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "service" in data
    assert data["service"] == "day02"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_hello_endpoint():
    """Test the hello endpoint"""
    response = client.get("/hello")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Hello from day02"

def test_get_config_endpoint():
    """Test the config endpoint"""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_get_metrics_endpoint():
    """Test the metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "request_count" in data