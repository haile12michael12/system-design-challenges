import pytest
from unittest.mock import patch, AsyncMock

from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def mock_user_repo():
    with patch("app.services.user_service.UserRepository") as mock:
        yield mock


@pytest.fixture
def mock_follow_repo():
    with patch("app.services.user_service.FollowRepository") as mock:
        yield mock


@pytest.fixture
def mock_cache():
    with patch("app.services.user_service.cache_get") as mock_get, \
         patch("app.services.user_service.cache_set") as mock_set, \
         patch("app.services.user_service.cache_delete") as mock_delete:
        yield mock_get, mock_set, mock_delete


@pytest.mark.asyncio
async def test_create_user(user_service, mock_user_repo, mock_cache):
    """Test creating a user"""
    # Arrange
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        bio="Test bio",
        password="testpassword"
    )
    
    mock_user = AsyncMock()
    mock_user.id = "user_123"
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.bio = "Test bio"
    
    mock_user_repo().create_user = AsyncMock(return_value=mock_user)
    
    # Act
    result = await user_service.create_user(user_data)
    
    # Assert
    assert result.username == "testuser"
    mock_user_repo().create_user.assert_called_once()
    # Verify password was hashed
    called_user_data = mock_user_repo().create_user.call_args[0][0]
    assert called_user_data.password != "testpassword"


@pytest.mark.asyncio
async def test_get_user(user_service, mock_user_repo, mock_cache):
    """Test getting a user"""
    # Arrange
    user_id = "user_123"
    mock_user = AsyncMock()
    mock_user.id = user_id
    mock_user.username = "testuser"
    
    mock_user_repo().get_user = AsyncMock(return_value=mock_user)
    mock_cache[0].return_value = None  # No cached value
    
    # Act
    result = await user_service.get_user(user_id)
    
    # Assert
    assert result.id == user_id
    mock_user_repo.return_value.get_user.assert_called_once_with(user_id)
    mock_cache[1].assert_called_once()  # Cache set was called