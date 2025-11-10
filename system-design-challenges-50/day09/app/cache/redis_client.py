"""
Redis Client
"""
import redis.asyncio as redis
from app.core.config import settings
from typing import Optional

class RedisClient:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
    
    async def get(self, key: str):
        return await self.redis_client.get(key)
    
    async def set(self, key: str, value: str, ex: Optional[int] = None):
        return await self.redis_client.set(key, value, ex=ex)
    
    async def delete(self, key: str):
        return await self.redis_client.delete(key)
    
    async def close(self):
        await self.redis_client.close()

# Global Redis client instance
redis_client = RedisClient()