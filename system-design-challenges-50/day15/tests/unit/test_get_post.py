import pytest
from app.application.queries.get_post import GetPostQuery
from app.application.handlers.query_handlers.get_post_handler import GetPostHandler

def test_get_post_query():
    """Test creating a get post query."""
    query = GetPostQuery(post_id="test-id")
    assert query.post_id == "test-id"

def test_get_post_handler():
    """Test get post handler."""
    query = GetPostQuery(post_id="test-id")
    handler = GetPostHandler()
    post = handler.handle(query)
    
    # In our current implementation, this returns None
    assert post is None