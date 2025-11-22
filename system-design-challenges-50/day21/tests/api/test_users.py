import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.schemas.user import UserCreate, UserResponse

client = TestClient(app)


@pytest.fixture
def mock_user_service():
    with patch("app.api.users.UserService") as mock:
        yield mock


def test_create_user(mock_user_service):
    """Test creating a new user"""
    # Arrange
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "bio": "Test bio",
        "password": "testpassword"
    }
    
    mock_user = UserResponse(
        id="user_123",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        bio="Test bio",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )
    
    mock_user_service.return_value.create_user = AsyncMock(return_value=mock_user)
    
    # Act
    response = client.post("/api/v1/users/", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    mock_user_service.return_value.create_user.assert_called_once()


def test_get_user(mock_user_service):
    """Test getting a user by ID"""
    # Arrange
    user_id = "user_123"
    mock_user = UserResponse(
        id="user_123",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        bio="Test bio",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )
    
    mock_user_service.return_value.get_user = AsyncMock(return_value=mock_user)
    
    # Act
    response = client.get(f"/api/v1/users/{user_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    mock_user_service.return_value.get_user.assert_called_once_with(user_id)