from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sensors.urls")),
    path("api/weather/", include("weather.urls")),
]
