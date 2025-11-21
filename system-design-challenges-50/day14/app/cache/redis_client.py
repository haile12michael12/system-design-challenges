import redis
from ..core.config import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL)
    
    def get(self, key: str):
        """Get a value from Redis"""
        return self.client.get(key)
    
    def set(self, key: str, value: str, expire: int = 3600):
        """Set a value in Redis"""
        return self.client.set(key, value, ex=expire)
    
    def delete(self, key: str):
        """Delete a key from Redis"""
        return self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis"""
        return self.client.exists(key)

# Global Redis client instance
redis_client = RedisClient()