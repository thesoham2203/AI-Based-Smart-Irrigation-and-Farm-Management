from __future__ import annotations
from django.db import models


class SensorReading(models.Model):
    timestamp = models.DateTimeField()
    field_id = models.CharField(max_length=64)
    crop_stage = models.CharField(max_length=64, blank=True, null=True)
    moisture = models.FloatField()
    temperature_c = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    action = models.CharField(max_length=16, blank=True, null=True, help_text="Action decided: IRRIGATE/SKIP")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class IrrigationEvent(models.Model):
    field_id = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=128, blank=True, null=True)

    @property
    def duration_seconds(self):
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
