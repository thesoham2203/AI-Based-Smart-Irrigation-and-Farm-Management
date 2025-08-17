from rest_framework import serializers
from .models import SensorReading, IrrigationEvent


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = [
            "id",
            "timestamp",
            "field_id",
            "crop_stage",
            "moisture",
            "temperature_c",
            "humidity",
            "action",
        ]


class IrrigationEventSerializer(serializers.ModelSerializer):
    duration_seconds = serializers.ReadOnlyField()

    class Meta:
        model = IrrigationEvent
        fields = ["id", "field_id", "start_time", "end_time", "reason", "duration_seconds"]
