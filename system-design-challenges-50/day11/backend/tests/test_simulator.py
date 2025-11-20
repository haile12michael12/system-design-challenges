import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..app.db.models import SimulationRequest

client = TestClient(app)

def test_start_simulation():
    """Test starting a simulation"""
    simulation_request = SimulationRequest(
        instances=2,
        workload=50,
        scaling_type="horizontal"
    )
    
    response = client.post("/api/v1/simulate", json=simulation_request.dict())
    assert response.status_code == 200
    assert "simulation_id" in response.json()
    assert "status" in response.json()

def test_get_simulation():
    """Test getting simulation results"""
    # Test with a mock simulation ID
    response = client.get("/api/v1/simulate/12345")
    assert response.status_code == 200
    assert "simulation_id" in response.json()
    assert "status" in response.json()