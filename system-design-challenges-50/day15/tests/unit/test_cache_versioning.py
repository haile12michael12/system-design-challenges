import pytest
from app.infrastructure.cache.versioning import CacheVersioning

def test_get_key_with_version():
    """Test getting key with version."""
    key = CacheVersioning.get_key_with_version("test-key", "v1")
    assert key == "test-key:v1"

def test_get_key_with_default_version():
    """Test getting key with default version."""
    key = CacheVersioning.get_key_with_version("test-key")
    assert key == "test-key:v1"

def test_get_post_key():
    """Test getting post key."""
    key = CacheVersioning.get_post_key("post-123", "v2")
    assert key == "post:post-123:v2"

def test_get_feed_key():
    """Test getting feed key."""
    key = CacheVersioning.get_feed_key("user-456", "v3")
    assert key == "feed:user-456:v3"