from django.db import models


class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    temperature_c = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(default=0.0)  # mm
    weather_description = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["location", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.location} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class WeatherForecast(models.Model):
    location = models.CharField(max_length=100)
    forecast_timestamp = models.DateTimeField()
    temperature_c = models.FloatField()
    humidity = models.FloatField()
    precipitation_probability = models.FloatField(default=0.0)  # percentage
    precipitation_amount = models.FloatField(default=0.0)  # mm
    weather_description = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-forecast_timestamp"]
        indexes = [
            models.Index(fields=["location", "-forecast_timestamp"]),
        ]
