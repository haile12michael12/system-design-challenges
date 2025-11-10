"""
Redis Connection and Caching Utilities
"""
import redis.asyncio as redis
import json
from typing import Optional, Any
from app.core.config import settings

class RedisCache:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        return await self.redis_client.get(key)
    
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set key-value pair with optional TTL"""
        if ttl:
            return await self.redis_client.set(key, value, ex=ttl)
        return await self.redis_client.set(key, value)
    
    async def delete(self, key: str) -> int:
        """Delete key"""
        return await self.redis_client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return bool(await self.redis_client.exists(key))
    
    async def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set JSON value"""
        return await self.set(key, json.dumps(value), ttl)
    
    async def get_json(self, key: str) -> Optional[Any]:
        """Get JSON value"""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def close(self):
        """Close Redis connection"""
        await self.redis_client.close()

# Global Redis cache instance
redis_cache = RedisCache()