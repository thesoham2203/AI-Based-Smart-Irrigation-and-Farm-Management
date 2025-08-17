from django.contrib import admin
from .models import SensorReading, IrrigationEvent

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "field_id", "moisture", "temperature_c", "humidity", "action")
    list_filter = ("field_id", "crop_stage")
    ordering = ("-timestamp",)

@admin.register(IrrigationEvent)
class IrrigationEventAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "duration_seconds", "field_id", "reason")
    ordering = ("-start_time",)
