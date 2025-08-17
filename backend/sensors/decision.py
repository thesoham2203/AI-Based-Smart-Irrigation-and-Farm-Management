from django.conf import settings
from weather.services import WeatherService


def decide_action(moisture: float, temperature: float = None, humidity: float = None, 
                 location: str = None, threshold: float = None) -> str:
    """Enhanced decision logic considering weather conditions."""
    
    # Use configured threshold or default
    threshold = threshold or getattr(settings, 'DEFAULT_MOISTURE_THRESHOLD', 35.0)
    
    # Basic moisture check
    if moisture >= threshold:
        return "SKIP"
    
    # Check weather conditions to avoid irrigation before rain
    if WeatherService.will_rain_today(location):
        return "SKIP"  # Don't irrigate if rain expected
    
    # Consider temperature and humidity for evapotranspiration
    if temperature and humidity:
        # High temperature + low humidity = higher water need
        if temperature > 30 and humidity < 40:
            threshold += 5  # More aggressive irrigation
        elif temperature < 20 and humidity > 70:
            threshold -= 5  # Less aggressive irrigation
    
    return "IRRIGATE" if moisture < threshold else "SKIP"
