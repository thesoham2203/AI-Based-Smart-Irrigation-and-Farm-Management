from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SensorReading, IrrigationEvent
from .serializers import SensorReadingSerializer, IrrigationEventSerializer
from .decision import decide_action


class SensorReadingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        try:
            moisture = float(data.get("moisture"))
            temperature = data.get("temperature_c")
            humidity = data.get("humidity")
            field_id = data.get("field_id")
        except (TypeError, ValueError):
            return Response({"error": "Invalid sensor data"}, status=400)
        
        # Enhanced decision making
        action_decision = decide_action(
            moisture=moisture,
            temperature=float(temperature) if temperature else None,
            humidity=float(humidity) if humidity else None,
            location=field_id
        )
        data["action"] = action_decision
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["get"], url_path="latest")
    def latest(self, request):
        obj = self.get_queryset().first()
        if not obj:
            return Response({}, status=200)
        return Response(self.get_serializer(obj).data)

    @action(detail=False, methods=["get"], url_path="chart-data")
    def chart_data(self, request):
        """Return last 24 hours of data for charts."""
        since = datetime.now() - timedelta(hours=24)
        readings = self.get_queryset().filter(timestamp__gte=since)[:100]
        return Response(self.get_serializer(readings, many=True).data)


class IrrigationEventViewSet(viewsets.ModelViewSet):
    queryset = IrrigationEvent.objects.all()
    serializer_class = IrrigationEventSerializer

    @action(detail=False, methods=["post"], url_path="start")
    def start(self, request):
        field_id = request.data.get("field_id", "default")
        reason = request.data.get("reason")
        event = IrrigationEvent.objects.create(
            field_id=field_id, 
            start_time=datetime.now(), 
            reason=reason
        )
        return Response(IrrigationEventSerializer(event).data, status=201)

    @action(detail=False, methods=["post"], url_path="stop")
    def stop(self, request):
        event_id = request.data.get("event_id")
        try:
            event = IrrigationEvent.objects.get(id=event_id, end_time__isnull=True)
        except IrrigationEvent.DoesNotExist:
            return Response({"error": "Active irrigation event not found"}, status=404)
        
        event.end_time = datetime.now()
        event.save()
        return Response(IrrigationEventSerializer(event).data)

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        """Get currently active irrigation events."""
        active_events = self.get_queryset().filter(end_time__isnull=True)
        return Response(self.get_serializer(active_events, many=True).data)
