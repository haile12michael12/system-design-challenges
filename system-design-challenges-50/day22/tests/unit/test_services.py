import pytest
from unittest.mock import patch, MagicMock
from app.services.feed_service import get_personalized_feed, get_explore_feed
from app.services.post_service import create_post, get_post, update_post, delete_post
from app.services.auth_service import verify_password, get_password_hash
from app.schemas.feed import PersonalizedFeedRequest, ExploreFeedRequest

@patch('app.services.feed_service.get_cached_feed')
@patch('app.services.feed_service.set_cached_feed')
def test_get_personalized_feed(mock_set_cached_feed, mock_get_cached_feed):
    """Test personalized feed retrieval"""
    # Mock cache miss
    mock_get_cached_feed.return_value = None
    
    # Create a mock database session
    mock_db = MagicMock()
    
    # Create request
    request = PersonalizedFeedRequest(user_id=1, limit=10)
    
    # Call the function
    result = get_personalized_feed(mock_db, request)
    
    # Verify results
    assert result is not None
    assert isinstance(result.items, list)
    assert result.has_more == False

@patch('app.services.feed_service.get_cached_feed')
@patch('app.services.feed_service.set_cached_feed')
def test_get_explore_feed(mock_set_cached_feed, mock_get_cached_feed):
    """Test explore feed retrieval"""
    # Mock cache miss
    mock_get_cached_feed.return_value = None
    
    # Create a mock database session
    mock_db = MagicMock()
    
    # Create request
    request = ExploreFeedRequest(limit=10, offset=0)
    
    # Call the function
    result = get_explore_feed(mock_db, request)
    
    # Verify results
    assert result is not None
    assert isinstance(result.items, list)
    assert result.has_more == False

def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword"
    
    # Hash the password
    hashed = get_password_hash(password)
    assert hashed is not None
    assert hashed != password
    
    # Verify the password
    assert verify_password(password, hashed) is True
    
    # Verify with wrong password
    assert verify_password("wrongpassword", hashed) is False

@patch('app.models.post.Post')
def test_create_post(mock_post):
    """Test post creation"""
    # Create a mock database session
    mock_db = MagicMock()
    
    # Create post data
    post_data = {
        "content": "Test post content",
        "media_url": "http://example.com/image.jpg"
    }
    
    # Create a mock post instance
    mock_post_instance = MagicMock()
    mock_post_instance.id = 1
    mock_post_instance.author_id = 123
    mock_post_instance.content = "Test post content"
    mock_post_instance.media_url = "http://example.com/image.jpg"
    
    # Configure the mock
    mock_post.return_value = mock_post_instance
    
    # Call the function
    result = create_post(mock_db, post_data, 123)
    
    # Verify results
    assert result is not None
    assert result.author_id == 123
    assert result.content == "Test post content"
    
    # Verify database operations
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()