"""
Replication Tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_replicate_data():
    """Test data replication endpoint"""
    response = client.post("/replicate/", json={
        "source_region": "us-east-1",
        "target_region": "us-west-1",
        "keys": ["key1", "key2", "key3"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["replicated_keys"] == 3

def test_sync_region():
    """Test region sync endpoint"""
    response = client.post("/replicate/sync", json={
        "region_id": "us-west-1",
        "timestamp": 1234567890.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"