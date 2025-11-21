import redis
from ...config import settings

class RedisClient:
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL)
    
    def get(self, key: str):
        return self.client.get(key)
    
    def set(self, key: str, value: str, expire: int = 3600):
        return self.client.set(key, value, ex=expire)
    
    def delete(self, key: str):
        return self.client.delete(key)

redis_client = RedisClient()