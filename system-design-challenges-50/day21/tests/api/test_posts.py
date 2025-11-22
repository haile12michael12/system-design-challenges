import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.schemas.post import PostCreate, PostResponse

client = TestClient(app)


@pytest.fixture
def mock_post_service():
    with patch("app.api.posts.PostService") as mock:
        yield mock


def test_create_post(mock_post_service):
    """Test creating a new post"""
    # Arrange
    post_data = {
        "content": "This is a test post",
        "media_url": "https://example.com/image.jpg"
    }
    
    mock_post = PostResponse(
        id="post_123",
        author_id="user_123",
        content="This is a test post",
        media_url="https://example.com/image.jpg",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        likes_count=0,
        comments_count=0
    )
    
    mock_post_service.return_value.create_post = AsyncMock(return_value=mock_post)
    
    # Act
    response = client.post("/api/v1/posts/", json=post_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["content"] == "This is a test post"
    mock_post_service.return_value.create_post.assert_called_once()


def test_get_post(mock_post_service):
    """Test getting a post by ID"""
    # Arrange
    post_id = "post_123"
    mock_post = PostResponse(
        id="post_123",
        author_id="user_123",
        content="This is a test post",
        media_url="https://example.com/image.jpg",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        likes_count=0,
        comments_count=0
    )
    
    mock_post_service.return_value.get_post = AsyncMock(return_value=mock_post)
    
    # Act
    response = client.get(f"/api/v1/posts/{post_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == post_id
    mock_post_service.return_value.get_post.assert_called_once_with(post_id)