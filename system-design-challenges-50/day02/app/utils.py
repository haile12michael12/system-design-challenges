import time
import logging
import asyncio
from typing import Any, Callable, Awaitable
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def timing_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to time function execution"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def retry_async(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry async functions"""
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = Exception("Unknown error")
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            raise last_exception
        return wrapper
    return decorator

def format_weather_data(weather_data: dict) -> dict:
    """Format weather data for display"""
    # Convert temperature from Kelvin to Celsius if needed
    if 'temp' in weather_data:
        weather_data['temp_celsius'] = round(weather_data['temp'] - 273.15, 2)
        weather_data['temp_fahrenheit'] = round((weather_data['temp'] - 273.15) * 9/5 + 32, 2)
    
    # Format timestamp
    if 'timestamp' in weather_data:
        weather_data['formatted_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_data['timestamp']))
    
    return weather_data

def validate_city_name(city: str) -> bool:
    """Validate city name format"""
    # Basic validation - check if city name is not empty and contains only letters, spaces, and hyphens
    if not city or not isinstance(city, str):
        return False
    return all(c.isalpha() or c.isspace() or c == '-' for c in city)

def calculate_uptime(start_time: float) -> str:
    """Calculate uptime and return as a formatted string"""
    uptime_seconds = time.time() - start_time
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    
    return f"{days}d {hours}h {minutes}m {seconds}s"