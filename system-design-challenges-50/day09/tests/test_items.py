"""
Items Tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    """Test creating an item"""
    response = client.post("/items/", json={"name": "Test Item", "price": 10.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.0

def test_get_item():
    """Test getting an item"""
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data

def test_list_items():
    """Test listing items"""
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_item():
    """Test updating an item"""
    response = client.put("/items/1", json={"name": "Updated Item", "price": 20.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["price"] == 20.0

def test_delete_item():
    """Test deleting an item"""
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data