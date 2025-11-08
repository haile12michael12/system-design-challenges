import pytest
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService
from app.db.models import User
from app.utils.validation_utils import validate_email, validate_password

def test_user_create():
    """
    Test creating a user
    """
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="securepassword123"
    )
    
    # In a real test, you would mock the database session
    # and verify the user is created correctly
    assert user_data.username == "testuser"
    assert user_data.email == "test@example.com"
    assert user_data.password == "securepassword123"

def test_email_validation():
    """
    Test email validation
    """
    valid_email = "test@example.com"
    invalid_email = "invalid-email"
    
    assert validate_email(valid_email) == True
    assert validate_email(invalid_email) == False

def test_password_validation():
    """
    Test password validation
    """
    strong_password = "securepassword123"
    weak_password = "123"
    
    assert validate_password(strong_password) == True
    assert validate_password(weak_password) == False

if __name__ == "__main__":
    pytest.main()