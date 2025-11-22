import pytest
from unittest.mock import patch, AsyncMock

from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate


@pytest.fixture
def post_service():
    return PostService()


@pytest.fixture
def mock_post_repo():
    with patch("app.services.post_service.PostRepository") as mock:
        yield mock


@pytest.fixture
def mock_cache():
    with patch("app.services.post_service.cache_get") as mock_get, \
         patch("app.services.post_service.cache_set") as mock_set, \
         patch("app.services.post_service.cache_delete") as mock_delete:
        yield mock_get, mock_set, mock_delete


@pytest.mark.asyncio
async def test_create_post(post_service, mock_post_repo, mock_cache):
    """Test creating a post"""
    # Arrange
    post_data = PostCreate(
        content="This is a test post",
        media_url="https://example.com/image.jpg"
    )
    
    user_id = "user_123"
    mock_post = AsyncMock()
    mock_post.id = "post_123"
    mock_post.author_id = user_id
    mock_post.content = "This is a test post"
    mock_post.media_url = "https://example.com/image.jpg"
    
    mock_post_repo().create_post = AsyncMock(return_value=mock_post)
    
    # Act
    result = await post_service.create_post(post_data, user_id)
    
    # Assert
    assert result.content == "This is a test post"
    mock_post_repo().create_post.assert_called_once()
    mock_cache[1].assert_called_once()  # Cache set was called


@pytest.mark.asyncio
async def test_get_post(post_service, mock_post_repo, mock_cache):
    """Test getting a post"""
    # Arrange
    post_id = "post_123"
    mock_post = AsyncMock()
    mock_post.id = post_id
    mock_post.content = "This is a test post"
    
    mock_post_repo().get_post = AsyncMock(return_value=mock_post)
    mock_cache[0].return_value = None  # No cached value
    
    # Act
    result = await post_service.get_post(post_id)
    
    # Assert
    assert result.id == post_id
    mock_post_repo().get_post.assert_called_once_with(post_id)
    mock_cache[1].assert_called_once()  # Cache set was called