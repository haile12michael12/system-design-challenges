import pytest
import asyncio
from datetime import datetime
from app.models import WeatherData, Location
from app.services import WeatherService

@pytest.fixture
def weather_service():
    """Create a WeatherService instance for testing"""
    return WeatherService()

@pytest.mark.asyncio
async def test_get_current_weather(weather_service):
    """Test getting current weather data"""
    city = "Test City"
    weather = await weather_service.get_current_weather(city)
    
    assert isinstance(weather, WeatherData)
    assert weather.city == city
    assert isinstance(weather.temperature, float)
    assert isinstance(weather.humidity, float)
    assert isinstance(weather.pressure, float)
    assert isinstance(weather.wind_speed, float)
    assert isinstance(weather.timestamp, datetime)

@pytest.mark.asyncio
async def test_get_forecast(weather_service):
    """Test getting weather forecast"""
    city = "Test City"
    days = 5
    forecast = await weather_service.get_forecast(city, days)
    
    assert forecast.city == city
    assert len(forecast.forecast) == days
    for weather in forecast.forecast:
        assert isinstance(weather, WeatherData)
        assert weather.city == city

@pytest.mark.asyncio
async def test_update_weather_data(weather_service):
    """Test updating weather data"""
    city = "Test City"
    weather_data = WeatherData(
        id=1,
        city=city,
        temperature=25.0,
        humidity=60.0,
        pressure=1013.25,
        wind_speed=10.0,
        timestamp=datetime.now(),
        condition="Sunny"
    )
    
    await weather_service.update_weather_data(city, weather_data)
    
    # Verify data was added
    assert city in weather_service.weather_data
    assert len(weather_service.weather_data[city]) == 1

def test_add_location(weather_service):
    """Test adding a location"""
    location = Location(
        city="Test City",
        country="Test Country",
        latitude=0.0,
        longitude=0.0
    )
    
    weather_service.add_location(location)
    
    assert location.city in weather_service.locations
    assert weather_service.locations[location.city] == location