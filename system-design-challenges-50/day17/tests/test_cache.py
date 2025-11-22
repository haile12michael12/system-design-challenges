import json
import pytest
from unittest.mock import Mock, patch
from typing import List

from app.domain.entities.post_entity import PostEntity
from app.cache.post_cache import PostCache
from app.cache.feed_cache import FeedCache


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
            id=f"post_{i}",
            user_id=f"user_{i % 5}",
            content=f"Content of post {i}",
            is_published=True
        )
        for i in range(5)
    ]


@pytest.mark.asyncio
async def test_cache_post(mock_post_entity):
    """Test caching a post."""
    # Arrange
    with patch('app.cache.post_cache.get_redis_client') as mock_redis_factory:
        mock_redis_client = Mock()
        mock_redis_factory.return_value = mock_redis_client
        mock_redis_client.set.return_value = True
        
        cache = PostCache()
        
        # Act
        result = await cache.cache_post(mock_post_entity)
        
        # Assert
        assert result is True
        mock_redis_client.set.assert_called_once()
        # Check that the key is correctly formatted
        call_args = mock_redis_client.set.call_args
        key = call_args[0][0]
        assert key == f"post:{mock_post_entity.id}"


@pytest.mark.asyncio
async def test_get_post_from_cache(mock_post_entity):
    """Test getting a post from cache."""
    # Arrange
    with patch('app.cache.post_cache.get_redis_client') as mock_redis_factory:
        mock_redis_client = Mock()
        mock_redis_factory.return_value = mock_redis_client
        mock_redis_client.get.return_value = mock_post_entity.json()
        
        cache = PostCache()
        
        # Act
        result = await cache.get_post(mock_post_entity.id)
        
        # Assert
        assert result is not None
        assert result.id == mock_post_entity.id
        assert result.content == mock_post_entity.content
        mock_redis_client.get.assert_called_once_with(f"post:{mock_post_entity.id}")


@pytest.mark.asyncio
async def test_cache_feed(mock_post_entities):
    """Test caching a feed."""
    # Arrange
    with patch('app.cache.feed_cache.get_redis_client') as mock_redis_factory:
        mock_redis_client = Mock()
        mock_redis_factory.return_value = mock_redis_client
        mock_redis_client.set.return_value = True
        
        cache = FeedCache()
        
        # Act
        result = await cache.cache_feed("test_user_id", mock_post_entities, page=1, size=10)
        
        # Assert
        assert result is True
        mock_redis_client.set.assert_called_once()
        # Check that the key is correctly formatted
        call_args = mock_redis_client.set.call_args
        key = call_args[0][0]
        assert key == "feed:test_user_id:page:1:size:10"


@pytest.mark.asyncio
async def test_get_feed_from_cache(mock_post_entities):
    """Test getting a feed from cache."""
    # Arrange
    with patch('app.cache.feed_cache.get_redis_client') as mock_redis_factory:
        mock_redis_client = Mock()
        mock_redis_factory.return_value = mock_redis_client
        
        # Mock the JSON response from Redis
        feed_data = {
            "posts": [post.dict() for post in mock_post_entities],
            "user_id": "test_user_id",
            "page": 1,
            "size": 10
        }
        mock_redis_client.get.return_value = json.dumps(feed_data)
        
        cache = FeedCache()
        
        # Act
        result = await cache.get_feed("test_user_id", page=1, size=10)
        
        # Assert
        assert result is not None
        assert len(result) == len(mock_post_entities)
        for i, post in enumerate(result):
            assert post.id == mock_post_entities[i].id
            assert post.content == mock_post_entities[i].content
        mock_redis_client.get.assert_called_once_with("feed:test_user_id:page:1:size:10")


if __name__ == "__main__":
    pytest.main([__file__])