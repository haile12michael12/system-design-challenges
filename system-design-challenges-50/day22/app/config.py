import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/feed_db")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Kafka
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Feature Flags
    feature_cache_invalidation: bool = os.getenv("FEATURE_CACHE_INVALIDATION", "true").lower() == "true"
    feature_rollup_processing: bool = os.getenv("FEATURE_ROLLUP_PROCESSING", "true").lower() == "true"
    feature_cost_optimization: bool = os.getenv("FEATURE_COST_OPTIMIZATION", "true").lower() == "true"
    
    # Performance
    cache_ttl_feed: int = int(os.getenv("CACHE_TTL_FEED", "300"))
    cache_ttl_user: int = int(os.getenv("CACHE_TTL_USER", "3600"))
    batch_size_feed_processing: int = int(os.getenv("BATCH_SIZE_FEED_PROCESSING", "100"))

    class Config:
        env_file = ".env"

settings = Settings()