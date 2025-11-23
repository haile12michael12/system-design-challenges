import pytest
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from app.services.auth_service import register_user, authenticate_user, create_access_token

def test_user_registration(test_db):
    """Test user registration flow"""
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="securepassword"
    )
    
    user = register_user(test_db, user_data)
    
    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.hashed_password is not None
    # Password should be hashed, so it shouldn't match the original
    assert user.hashed_password != "securepassword"

def test_user_authentication(test_db):
    """Test user authentication flow"""
    # First register a user
    user_data = UserCreate(
        username="authuser",
        email="authuser@example.com",
        password="authpassword"
    )
    user = register_user(test_db, user_data)
    
    # Then authenticate the user
    authenticated_user = authenticate_user(test_db, "authuser", "authpassword")
    
    assert authenticated_user is not None
    assert authenticated_user.id == user.id
    assert authenticated_user.username == user.username

def test_invalid_credentials(test_db):
    """Test authentication with invalid credentials"""
    # Register a user
    user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword"
    )
    register_user(test_db, user_data)
    
    # Try to authenticate with wrong password
    authenticated_user = authenticate_user(test_db, "testuser", "wrongpassword")
    assert authenticated_user is None
    
    # Try to authenticate with wrong username
    authenticated_user = authenticate_user(test_db, "wronguser", "testpassword")
    assert authenticated_user is None

def test_jwt_token_creation():
    """Test JWT token creation"""
    user_data = {"sub": "123", "username": "testuser"}
    token = create_access_token(user_data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0