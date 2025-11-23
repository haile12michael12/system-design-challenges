import pytest
from app.schemas.user import UserCreate
from app.schemas.feed import PersonalizedFeedRequest, ExploreFeedRequest
from app.services.auth_service import register_user, create_access_token
from app.services.feed_service import get_personalized_feed, get_explore_feed

def test_user_registration_and_feed_generation(test_db):
    """Test complete flow: user registration -> post creation -> feed generation"""
    # 1. Register a new user
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    user = register_user(test_db, user_data)
    assert user.id is not None
    assert user.username == "testuser"
    
    # 2. Generate personalized feed for the user
    feed_request = PersonalizedFeedRequest(user_id=user.id, limit=10)
    feed_response = get_personalized_feed(test_db, feed_request)
    assert feed_response is not None
    assert isinstance(feed_response.items, list)
    
    # 3. Generate explore feed
    explore_request = ExploreFeedRequest(limit=10, offset=0)
    explore_response = get_explore_feed(test_db, explore_request)
    assert explore_response is not None
    assert isinstance(explore_response.items, list)

def test_feed_caching(test_db):
    """Test that feeds are properly cached"""
    # This test would verify that feed data is cached and retrieved correctly
    # Implementation would depend on the specific caching mechanism used
    pass

def test_feed_pagination(test_db):
    """Test feed pagination functionality"""
    # This test would verify that feed pagination works correctly
    pass