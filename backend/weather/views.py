from rest_framework.views import APIView
from rest_framework.response import Response
from .services import WeatherService


class WeatherDataView(APIView):
    def get(self, request):
        """Get current weather data."""
        location = request.GET.get('location')
        weather_data = WeatherService.fetch_current_weather(location)
        return Response(weather_data)
