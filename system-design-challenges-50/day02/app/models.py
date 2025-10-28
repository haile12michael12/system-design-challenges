from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WeatherData(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    timestamp: datetime
    condition: str

class Location(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float

class ForecastData(BaseModel):
    city: str
    forecast: List[WeatherData]
    last_updated: datetime

class UserPreferences(BaseModel):
    user_id: int
    favorite_cities: List[str]
    temperature_unit: str  # Celsius or Fahrenheit
    notifications_enabled: bool