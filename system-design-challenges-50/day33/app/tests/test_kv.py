"""
Key-Value Store Tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_key_value():
    """Test creating a key-value pair"""
    response = client.post("/kv/", json={"key": "test_key", "value": "test_value"})
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "test_key"
    assert data["value"] == "test_value"

def test_get_key_value():
    """Test getting a key-value pair"""
    # First create a key
    client.post("/kv/", json={"key": "test_key", "value": "test_value"})
    
    # Then retrieve it
    response = client.get("/kv/test_key")
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "test_key"
    assert data["value"] == "test_value"

def test_update_key_value():
    """Test updating a key-value pair"""
    # First create a key
    client.post("/kv/", json={"key": "test_key", "value": "test_value"})
    
    # Then update it
    response = client.put("/kv/test_key", json={"key": "test_key", "value": "updated_value"})
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "test_key"
    assert data["value"] == "updated_value"

def test_delete_key_value():
    """Test deleting a key-value pair"""
    # First create a key
    client.post("/kv/", json={"key": "test_key", "value": "test_value"})
    
    # Then delete it
    response = client.delete("/kv/test_key")
    assert response.status_code == 200