import pytest
from app.application.commands.create_post import CreatePostCommand
from app.application.handlers.command_handlers.create_post_handler import CreatePostHandler
from app.domain.entities.post import Post

def test_create_post_command():
    """Test creating a post command."""
    command = CreatePostCommand(content="Test content", author="Test author")
    assert command.content == "Test content"
    assert command.author == "Test author"

def test_create_post_handler():
    """Test creating a post handler."""
    command = CreatePostCommand(content="Test content", author="Test author")
    handler = CreatePostHandler()
    post = handler.handle(command)
    
    assert isinstance(post, Post)
    assert post.content == "Test content"
    assert post.author == "Test author"
    assert post.id is not None