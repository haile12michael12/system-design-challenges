from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time
from .models import WeatherData, Location, ForecastData, UserPreferences
from .services import weather_service
from .monitoring import metrics_collector
from .config import config

app = FastAPI(title="Day 2 - Weather Dashboard (Non-Functional Requirements Focus)")

# Add middleware to collect metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    metrics_collector.record_request(
        endpoint=str(request.url),
        response_time=process_time,
        success=response.status_code < 400
    )
    return response

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day02"
    timestamp: str

@app.get("/health", response_model=HealthResp)
async def health():
    from datetime import datetime
    return HealthResp(timestamp=datetime.now().isoformat())

@app.get("/")
async def root():
    return {"message": "Welcome to Day 2 - Weather Dashboard (Non-Functional Requirements Focus)"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day02"}

@app.get("/weather/{city}", response_model=WeatherData)
async def get_current_weather(city: str):
    """Get current weather for a specific city"""
    try:
        weather = await weather_service.get_current_weather(city)
        return weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")

@app.get("/forecast/{city}", response_model=ForecastData)
async def get_forecast(city: str, days: int = 5):
    """Get weather forecast for a specific city"""
    try:
        if days > 14:
            raise HTTPException(status_code=400, detail="Forecast limited to 14 days")
        forecast = await weather_service.get_forecast(city, days)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast data: {str(e)}")

@app.post("/preferences", response_model=UserPreferences)
async def set_user_preferences(preferences: UserPreferences):
    """Set user preferences for the weather dashboard"""
    # In a real app, this would save to a database
    return preferences

@app.get("/preferences/{user_id}", response_model=UserPreferences)
async def get_user_preferences(user_id: int):
    """Get user preferences for the weather dashboard"""
    # In a real app, this would fetch from a database
    # Returning mock data for now
    return UserPreferences(
        user_id=user_id,
        favorite_cities=["New York", "London", "Tokyo"],
        temperature_unit="Celsius",
        notifications_enabled=True
    )

@app.get("/metrics")
async def get_metrics():
    """Get application metrics"""
    return metrics_collector.get_metrics_summary()

@app.get("/config")
async def get_config():
    """Get application configuration"""
    return {
        "api_host": config.API_HOST,
        "api_port": config.API_PORT,
        "cache_ttl": config.CACHE_TTL,
        "max_concurrent_requests": config.MAX_CONCURRENT_REQUESTS,
        "rate_limit_per_minute": config.RATE_LIMIT_PER_MINUTE,
        "enable_metrics": config.ENABLE_METRICS,
        "log_level": config.LOG_LEVEL
    }
