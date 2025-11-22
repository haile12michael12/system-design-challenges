import pytest
from unittest.mock import patch
from typing import List

from app.domain.entities.post_entity import PostEntity
from app.domain.entities.feed_entity import FeedEntity
from app.domain.services.feed_reader import FeedReaderService


@pytest.fixture
def mock_feed_entity(mock_post_entities):
    """Create a mock feed entity."""
    return FeedEntity(
        posts=mock_post_entities,
        user_id="test_user_id",
        page=1,
        size=10
    )


@pytest.fixture
def mock_post_entities():
    """Create a list of mock post entities."""
    return [
        PostEntity(
            id=f"post_{i}",
            user_id=f"user_{i % 5}",
            content=f"Content of post {i}",
            is_published=True
        )
        for i in range(10)
    ]


@pytest.mark.asyncio
async def test_get_user_posts(mock_post_entities):
    """Test getting posts for a user."""
    # Arrange
    with patch('app.domain.services.feed_reader.PostRepository') as mock_repo:
        mock_repo.return_value.get_posts_by_user.return_value = mock_post_entities
        
        service = FeedReaderService()
        
        # Act
        result = await service.get_user_posts("test_user_id", page=1, size=10)
        
        # Assert
        assert len(result) == len(mock_post_entities)
        for i, post in enumerate(result):
            assert post.id == mock_post_entities[i].id
            assert post.user_id == mock_post_entities[i].user_id
            assert post.content == mock_post_entities[i].content
            assert post.is_published == mock_post_entities[i].is_published


@pytest.mark.asyncio
async def test_get_feed_with_cache(mock_post_entities):
    """Test getting feed with cache hit."""
    # Arrange
    with patch('app.domain.services.feed_reader.FeedCache') as mock_cache:
        mock_cache.return_value.get_feed.return_value = mock_post_entities
        
        service = FeedReaderService()
        
        # Act
        result = await service.get_feed(page=1, size=10)
        
        # Assert
        assert len(result) == len(mock_post_entities)
        mock_cache.return_value.get_feed.assert_called_once_with(1, 10)


@pytest.mark.asyncio
async def test_get_feed_without_cache(mock_post_entities):
    """Test getting feed with cache miss."""
    # Arrange
    with patch('app.domain.services.feed_reader.FeedCache') as mock_cache, \
         patch('app.domain.services.feed_reader.PostRepository') as mock_repo:
        
        mock_cache.return_value.get_feed.return_value = None
        mock_repo.return_value.get_feed_posts.return_value = mock_post_entities
        
        service = FeedReaderService()
        
        # Act
        result = await service.get_feed(page=1, size=10)
        
        # Assert
        assert len(result) == len(mock_post_entities)
        mock_cache.return_value.get_feed.assert_called_once_with(1, 10)
        mock_repo.return_value.get_feed_posts.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])