import pytest
from app.application.queries.feed_query import FeedQuery
from app.application.handlers.query_handlers.feed_query_handler import FeedQueryHandler

def test_feed_query():
    """Test creating a feed query."""
    query = FeedQuery(skip=10, limit=20)
    assert query.skip == 10
    assert query.limit == 20

def test_feed_query_default_values():
    """Test feed query default values."""
    query = FeedQuery()
    assert query.skip == 0
    assert query.limit == 10

def test_feed_query_handler():
    """Test feed query handler."""
    query = FeedQuery(skip=0, limit=10)
    handler = FeedQueryHandler()
    posts = handler.handle(query)
    
    # In our current implementation, this returns an empty list
    assert isinstance(posts, list)
    assert len(posts) == 0