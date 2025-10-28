import asyncio
from typing import List, Dict
from .models import WeatherData, Location, ForecastData
from datetime import datetime, timedelta

class WeatherService:
    def __init__(self):
        # In-memory storage for weather data
        self.weather_data: Dict[str, List[WeatherData]] = {}
        self.locations: Dict[str, Location] = {}
        
    async def get_current_weather(self, city: str) -> WeatherData:
        """Simulate fetching current weather data for a city"""
        # Simulate API call delay
        await asyncio.sleep(0.1)
        
        # Return mock data if city exists
        if city in self.weather_data and self.weather_data[city]:
            return self.weather_data[city][-1]  # Return latest data
        else:
            # Create mock data for new city
            return WeatherData(
                id=len(self.weather_data.get(city, [])) + 1,
                city=city,
                temperature=20.0 + (hash(city) % 10),  # Random temp between 20-30
                humidity=60.0 + (hash(city) % 20),     # Random humidity
                pressure=1013.25,                      # Standard pressure
                wind_speed=5.0 + (hash(city) % 10),    # Random wind speed
                timestamp=datetime.now(),
                condition="Sunny" if hash(city) % 2 == 0 else "Cloudy"
            )
    
    async def get_forecast(self, city: str, days: int = 5) -> ForecastData:
        """Generate a mock forecast for a city"""
        # Simulate API call delay
        await asyncio.sleep(0.2)
        
        forecast = []
        base_temp = 20.0 + (hash(city) % 10)
        
        for i in range(days):
            forecast.append(
                WeatherData(
                    id=i+1,
                    city=city,
                    temperature=base_temp + (i * 0.5),  # Gradually increasing temp
                    humidity=60.0 + (i * 2),            # Increasing humidity
                    pressure=1013.25 - (i * 0.5),       # Decreasing pressure
                    wind_speed=5.0 + (i * 0.3),         # Increasing wind
                    timestamp=datetime.now() + timedelta(days=i),
                    condition="Sunny" if (hash(city) + i) % 3 == 0 else "Cloudy" if (hash(city) + i) % 3 == 1 else "Rainy"
                )
            )
        
        return ForecastData(
            city=city,
            forecast=forecast,
            last_updated=datetime.now()
        )
    
    async def update_weather_data(self, city: str, data: WeatherData) -> None:
        """Update weather data for a city"""
        if city not in self.weather_data:
            self.weather_data[city] = []
        self.weather_data[city].append(data)
        
        # Keep only last 100 records per city
        if len(self.weather_data[city]) > 100:
            self.weather_data[city] = self.weather_data[city][-100:]
    
    def add_location(self, location: Location) -> None:
        """Add a location to the service"""
        self.locations[location.city] = location

# Global instance of the weather service
weather_service = WeatherService()