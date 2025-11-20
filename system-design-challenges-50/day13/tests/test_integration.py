import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.db.models import Payment

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_process_payment():
    """Test processing a payment"""
    payment_data = {
        "amount": 100.0,
        "currency": "USD",
        "payment_method": "credit_card",
        "card_number": "4111111111111111",
        "expiry_date": "12/25",
        "cvv": "123"
    }
    
    response = client.post("/api/v1/payments", json=payment_data)
    assert response.status_code == 200
    assert "payment_id" in response.json()
    assert response.json()["status"] == "pending"

def test_get_payment_status():
    """Test getting payment status"""
    # First create a payment
    payment_data = {
        "amount": 50.0,
        "currency": "USD",
        "payment_method": "paypal"
    }
    
    response = client.post("/api/v1/payments", json=payment_data)
    assert response.status_code == 200
    payment_id = response.json()["payment_id"]
    
    # Then get its status
    response = client.get(f"/api/v1/payments/{payment_id}")
    assert response.status_code == 200
    assert response.json()["payment_id"] == payment_id
    assert response.json()["status"] in ["pending", "processing", "completed", "failed"]

def test_get_nonexistent_payment():
    """Test getting status of a non-existent payment"""
    response = client.get("/api/v1/payments/999999")
    assert response.status_code == 200
    assert response.json()["status"] == "not_found"