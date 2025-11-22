import pytest
from unittest.mock import AsyncMock, Mock, patch
from typing import List

from app.domain.entities.post_entity import PostEntity
from app.domain.services.feed_writer import FeedWriterService
from app.domain.services.feed_reader import FeedReaderService
from app.schemas.post_schema import PostCreate, PostUpdate


@pytest.fixture
def mock_post_entity():
    """Create a mock post entity."""
    return PostEntity(
        id="test_post_id",
        user_id="test_user_id",
        content="Test post content",
        is_published=True
    )


@pytest.fixture
def mock_post_entities():
    """Create a list of mock post entities."""
    return [
        PostEntity(
            id=f"test_post_id_{i}",
            user_id=f"test_user_id_{i % 3}",
            content=f"Test post content {i}",
            is_published=True
        )
        for i in range(5)
    ]


@pytest.mark.asyncio
async def test_create_post(mock_post_entity):
    """Test creating a post."""
    # Arrange
    with patch('app.domain.services.feed_writer.PostRepository') as mock_repo, \
         patch('app.domain.services.feed_writer.EventPublisher') as mock_publisher:
        
        mock_repo.return_value.create_post.return_value = mock_post_entity
        mock_publisher.return_value.publish.return_value = True
        
        service = FeedWriterService()
        post_data = {
            "user_id": "test_user_id",
            "content": "Test post content"
        }
        
        # Act
        result = await service.create_post(post_data)
        
        # Assert
        assert result.id == mock_post_entity.id
        assert result.user_id == mock_post_entity.user_id
        assert result.content == mock_post_entity.content
        assert result.is_published == mock_post_entity.is_published


@pytest.mark.asyncio
async def test_get_post(mock_post_entity):
    """Test getting a post."""
    # Arrange
    with patch('app.domain.services.feed_reader.PostRepository') as mock_repo, \
         patch('app.domain.services.feed_reader.PostCache') as mock_cache:
        
        mock_cache.return_value.get_post.return_value = None
        mock_repo.return_value.get_post_by_id.return_value = mock_post_entity
        
        service = FeedReaderService()
        
        # Act
        result = await service.get_post("test_post_id")
        
        # Assert
        assert result.id == mock_post_entity.id
        assert result.user_id == mock_post_entity.user_id
        assert result.content == mock_post_entity.content
        assert result.is_published == mock_post_entity.is_published


@pytest.mark.asyncio
async def test_get_feed(mock_post_entities):
    """Test getting a feed."""
    # Arrange
    with patch('app.domain.services.feed_reader.PostRepository') as mock_repo, \
         patch('app.domain.services.feed_reader.FeedCache') as mock_cache:
        
        mock_cache.return_value.get_feed.return_value = None
        mock_repo.return_value.get_feed_posts.return_value = mock_post_entities
        
        service = FeedReaderService()
        
        # Act
        result = await service.get_feed(page=1, size=10)
        
        # Assert
        assert len(result) == len(mock_post_entities)
        for i, post in enumerate(result):
            assert post.id == mock_post_entities[i].id
            assert post.user_id == mock_post_entities[i].user_id
            assert post.content == mock_post_entities[i].content


if __name__ == "__main__":
    pytest.main([__file__])