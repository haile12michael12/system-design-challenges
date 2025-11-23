import redis
import json
from app.config import settings
from typing import Optional, Any

# Create Redis client
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

def get_cached_feed(key: str) -> Optional[str]:
    """Get cached feed data"""
    try:
        return redis_client.get(key)
    except Exception:
        return None

def set_cached_feed(key: str, data: str, ttl: int = settings.cache_ttl_feed):
    """Set cached feed data"""
    try:
        redis_client.setex(key, ttl, data)
    except Exception:
        pass

def invalidate_pattern(pattern: str) -> int:
    """Invalidate all keys matching a pattern"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except Exception:
        return 0

def get_key(key: str) -> Optional[Any]:
    """Get a value from Redis"""
    try:
        return redis_client.get(key)
    except Exception:
        return None

def set_key(key: str, value: Any, ttl: int = 3600):
    """Set a value in Redis"""
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        redis_client.setex(key, ttl, str(value))
    except Exception:
        pass