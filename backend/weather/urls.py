from django.urls import path
from .views import WeatherDataView

urlpatterns = [
    path("current/", WeatherDataView.as_view(), name="current-weather"),
]
