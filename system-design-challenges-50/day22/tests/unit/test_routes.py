import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.routes.auth import login_for_access_token, register_new_user
from app.routes.feed import get_user_feed, get_explore_feed_route
from app.routes.posts import create_new_post, read_post, update_existing_post, delete_existing_post
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.feed import PersonalizedFeedRequest, ExploreFeedRequest

def test_login_endpoint():
    """Test login endpoint"""
    # Create a mock database session
    mock_db = MagicMock()
    
    # Create login request
    form_data = LoginRequest(username="testuser", password="testpassword")
    
    # Mock the authenticate_user function
    with patch('app.routes.auth.authenticate_user') as mock_authenticate:
        # Configure the mock to return a user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_authenticate.return_value = mock_user
        
        # Mock the create_access_token function
        with patch('app.routes.auth.create_access_token') as mock_create_token:
            mock_create_token.return_value = "test_token"
            
            # Call the endpoint
            result = login_for_access_token(form_data, mock_db)
            
            # Verify results
            assert result is not None
            assert result["access_token"] == "test_token"
            assert result["token_type"] == "bearer"

def test_register_endpoint():
    """Test register endpoint"""
    # Create a mock database session
    mock_db = MagicMock()
    
    # Create register request
    user_data = RegisterRequest(
        username="newuser",
        email="newuser@example.com",
        password="newpassword"
    )
    
    # Mock the register_user function
    with patch('app.routes.auth.register_user') as mock_register:
        # Configure the mock to return a user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "newuser"
        mock_user.email = "newuser@example.com"
        mock_register.return_value = mock_user
        
        # Call the endpoint
        result = register_new_user(user_data, mock_db)
        
        # Verify results
        assert result is not None
        assert result.id == 1
        assert result.username == "newuser"

def test_create_post_endpoint():
    """Test create post endpoint"""
    # Create a mock database session
    mock_db = MagicMock()
    
    # Create post data
    post_data = {"content": "Test post"}
    
    # Create current user mock
    current_user = {"user_id": "1"}
    
    # Mock the create_post function
    with patch('app.routes.posts.create_post') as mock_create_post:
        # Configure the mock to return a post
        mock_post = MagicMock()
        mock_post.id = 1
        mock_post.content = "Test post"
        mock_create_post.return_value = mock_post
        
        # Call the endpoint
        result = create_new_post(post_data, mock_db, current_user)
        
        # Verify results
        assert result is not None
        assert result.id == 1

def test_get_post_endpoint():
    """Test get post endpoint"""
    # Create a mock database session
    mock_db = MagicMock()
    
    # Mock the get_post function
    with patch('app.routes.posts.get_post') as mock_get_post:
        # Configure the mock to return a post
        mock_post = MagicMock()
        mock_post.id = 1
        mock_post.content = "Test post"
        mock_get_post.return_value = mock_post
        
        # Call the endpoint
        result = read_post(1, mock_db)
        
        # Verify results
        assert result is not None
        assert result.id == 1

def test_get_post_endpoint_not_found():
    """Test get post endpoint when post is not found"""
    # Create a mock database session
    mock_db = MagicMock()
    
    # Mock the get_post function to return None
    with patch('app.routes.posts.get_post') as mock_get_post:
        mock_get_post.return_value = None
        
        # Call the endpoint and expect HTTPException
        with pytest.raises(HTTPException) as exc_info:
            read_post(999, mock_db)
        
        # Verify the exception
        assert exc_info.value.status_code == 404