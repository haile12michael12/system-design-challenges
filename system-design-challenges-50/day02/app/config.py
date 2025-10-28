import os
from typing import Optional

class Config:
    """Application configuration settings"""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/weatherdb")
    
    # Redis settings (for caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Weather API settings (in a real app, you'd use a real weather API)
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY")
    WEATHER_API_BASE_URL: str = os.getenv("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5")
    
    # Cache settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes default
    
    # Scaling settings
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "1000"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10000"))
    
    # Monitoring settings
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Availability settings
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))  # seconds
    
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    
    # Higher rate limits for production
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10000"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100000"))

# Configuration factory
def get_config(environment: str | None = None) -> Config:
    """Get configuration based on environment"""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Default config
config = get_config()