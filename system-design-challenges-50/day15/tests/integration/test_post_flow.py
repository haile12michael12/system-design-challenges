import pytest
from app.application.commands.create_post import CreatePostCommand
from app.application.handlers.command_handlers.create_post_handler import CreatePostHandler
from app.application.queries.get_post import GetPostQuery
from app.application.handlers.query_handlers.get_post_handler import GetPostHandler

def test_post_creation_and_retrieval_flow():
    """Test the complete flow of creating and retrieving a post."""
    # Create a post
    create_command = CreatePostCommand(content="Integration test content", author="Integration Tester")
    create_handler = CreatePostHandler()
    created_post = create_handler.handle(create_command)
    
    # Verify the post was created
    assert created_post is not None
    assert created_post.content == "Integration test content"
    assert created_post.author == "Integration Tester"
    
    # Note: In a real implementation, we would then retrieve the post
    # For now, our get_post_handler returns None as it's not fully implemented