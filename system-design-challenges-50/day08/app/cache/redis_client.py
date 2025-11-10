"""
Redis Connection Utility
"""
import redis.asyncio as redis
import os
from typing import Optional

# Redis URL from environment or default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisClient:
    def __init__(self):
        self.redis_client = redis.from_url(REDIS_URL)
    
    async def get(self, key: str):
        return await self.redis_client.get(key)
    
    async def set(self, key: str, value: str, ex: Optional[int] = None):
        return await self.redis_client.set(key, value, ex=ex)
    
    async def close(self):
        await self.redis_client.close()

# Global Redis client instance
redis_client = RedisClient()