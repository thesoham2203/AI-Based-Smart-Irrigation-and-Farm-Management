import requests
from datetime import datetime
from django.conf import settings
from .models import WeatherData, WeatherForecast


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    @classmethod
    def fetch_current_weather(cls, location: str = None) -> dict:
        """Fetch current weather data from OpenWeatherMap API."""
        if not settings.WEATHER_API_KEY:
            return {}
        
        location = location or settings.WEATHER_LOCATION
        url = f"{cls.BASE_URL}/weather"
        params = {
            "q": location,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}

    @classmethod
    def fetch_forecast(cls, location: str = None) -> dict:
        """Fetch 5-day weather forecast."""
        if not settings.WEATHER_API_KEY:
            return {}
        
        location = location or settings.WEATHER_LOCATION
        url = f"{cls.BASE_URL}/forecast"
        params = {
            "q": location,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}

    @classmethod
    def save_current_weather(cls, location: str = None) -> WeatherData:
        """Fetch and save current weather data."""
        data = cls.fetch_current_weather(location)
        if not data:
            return None
        
        weather_data = WeatherData.objects.create(
            location=data["name"],
            timestamp=datetime.fromtimestamp(data["dt"]),
            temperature_c=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            pressure=data["main"].get("pressure"),
            wind_speed=data.get("wind", {}).get("speed"),
            precipitation=data.get("rain", {}).get("1h", 0) + data.get("snow", {}).get("1h", 0),
            weather_description=data["weather"][0]["description"]
        )
        return weather_data

    @classmethod
    def will_rain_today(cls, location: str = None) -> bool:
        """Check if rain is expected in the next 12 hours."""
        forecast_data = cls.fetch_forecast(location)
        if not forecast_data or "list" not in forecast_data:
            return False
        
        # Check next 4 forecast periods (12 hours)
        for item in forecast_data["list"][:4]:
            if item.get("rain", {}).get("3h", 0) > 0:
                return True
        return False
