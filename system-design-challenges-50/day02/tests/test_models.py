import pytest
from datetime import datetime
from app.models import WeatherData, Location, ForecastData, UserPreferences

def test_weather_data_model():
    """Test WeatherData model creation"""
    weather = WeatherData(
        id=1,
        city="New York",
        temperature=25.5,
        humidity=60.0,
        pressure=1013.25,
        wind_speed=10.5,
        timestamp=datetime.now(),
        condition="Sunny"
    )
    
    assert weather.id == 1
    assert weather.city == "New York"
    assert weather.temperature == 25.5
    assert weather.humidity == 60.0
    assert weather.pressure == 1013.25
    assert weather.wind_speed == 10.5
    assert weather.condition == "Sunny"

def test_location_model():
    """Test Location model creation"""
    location = Location(
        city="London",
        country="UK",
        latitude=51.5074,
        longitude=-0.1278
    )
    
    assert location.city == "London"
    assert location.country == "UK"
    assert location.latitude == 51.5074
    assert location.longitude == -0.1278

def test_forecast_data_model():
    """Test ForecastData model creation"""
    weather_data = WeatherData(
        id=1,
        city="Paris",
        temperature=20.0,
        humidity=55.0,
        pressure=1015.0,
        wind_speed=8.0,
        timestamp=datetime.now(),
        condition="Cloudy"
    )
    
    forecast = ForecastData(
        city="Paris",
        forecast=[weather_data],
        last_updated=datetime.now()
    )
    
    assert forecast.city == "Paris"
    assert len(forecast.forecast) == 1
    assert forecast.forecast[0].city == "Paris"

def test_user_preferences_model():
    """Test UserPreferences model creation"""
    preferences = UserPreferences(
        user_id=123,
        favorite_cities=["New York", "London", "Tokyo"],
        temperature_unit="Celsius",
        notifications_enabled=True
    )
    
    assert preferences.user_id == 123
    assert "New York" in preferences.favorite_cities
    assert preferences.temperature_unit == "Celsius"
    assert preferences.notifications_enabled == True