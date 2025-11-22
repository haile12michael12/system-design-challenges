import pytest
from unittest.mock import patch

from app.domain.entities.user_entity import UserEntity
from app.domain.services.feed_writer import FeedWriterService
from app.domain.services.feed_reader import FeedReaderService


@pytest.fixture
def mock_user_entity():
    """Create a mock user entity."""
    return UserEntity(
        id="test_user_id",
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True
    )


@pytest.mark.asyncio
async def test_create_user(mock_user_entity):
    """Test creating a user."""
    # Arrange
    with patch('app.domain.services.feed_writer.UserRepository') as mock_repo, \
         patch('app.domain.services.feed_writer.get_password_hash') as mock_hash:
        
        mock_repo.return_value.create_user.return_value = mock_user_entity
        mock_hash.return_value = "hashed_password"
        
        service = FeedWriterService()
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "plaintext_password"
        }
        
        # Act
        result = await service.create_user(user_data)
        
        # Assert
        assert result.id == mock_user_entity.id
        assert result.username == mock_user_entity.username
        assert result.email == mock_user_entity.email
        assert result.is_active == mock_user_entity.is_active
        mock_hash.assert_called_once_with("plaintext_password")


@pytest.mark.asyncio
async def test_follow_user():
    """Test following a user."""
    # Arrange
    with patch('app.domain.services.feed_writer.UserRepository') as mock_repo, \
         patch('app.domain.services.feed_writer.EventPublisher') as mock_publisher:
        
        mock_repo.return_value.follow_user.return_value = True
        mock_publisher.return_value.publish.return_value = True
        
        service = FeedWriterService()
        
        # Act
        result = await service.follow_user("follower_id", "followed_id")
        
        # Assert
        assert result is True
        mock_repo.return_value.follow_user.assert_called_once_with("follower_id", "followed_id")


@pytest.mark.asyncio
async def test_unfollow_user():
    """Test unfollowing a user."""
    # Arrange
    with patch('app.domain.services.feed_writer.UserRepository') as mock_repo:
        mock_repo.return_value.unfollow_user.return_value = True
        
        service = FeedWriterService()
        
        # Act
        result = await service.unfollow_user("follower_id", "followed_id")
        
        # Assert
        assert result is True
        mock_repo.return_value.unfollow_user.assert_called_once_with("follower_id", "followed_id")


if __name__ == "__main__":
    pytest.main([__file__])