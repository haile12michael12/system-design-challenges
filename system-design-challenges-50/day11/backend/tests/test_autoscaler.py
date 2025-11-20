import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_scaling_recommendation():
    """Test autoscaling recommendation endpoint"""
    response = client.get("/api/v1/autoscale/recommend?current_instances=2&workload=50")
    assert response.status_code == 200
    assert "action" in response.json()
    assert "reason" in response.json()
    assert "current_instances" in response.json()
    assert "new_instances" in response.json()