import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.order_schemas import OrderCreate, OrderItemCreate

client = TestClient(app)

def test_create_order():
    """Test creating an order"""
    order_data = {
        "customer_id": 1,
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "price": 25.0
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == 1
    assert data["status"] == "pending"
    assert "id" in data

def test_get_order():
    """Test getting an order by ID"""
    response = client.get("/orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "customer_id" in data

def test_list_orders():
    """Test listing all orders"""
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0