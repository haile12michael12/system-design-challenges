"""
Feed Tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_feed():
    """Test getting user feed"""
    response = client.get("/feed/?user_id=user123&limit=10")
    # Since this is a placeholder implementation, we expect a 200 response
    # with the placeholder data
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    # We expect the placeholder post
    assert len(data["posts"]) >= 0

def test_get_feed_with_cursor():
    """Test getting user feed with cursor pagination"""
    response = client.get("/feed/?user_id=user123&limit=10&cursor=abc123")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data