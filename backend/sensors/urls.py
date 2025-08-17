from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SensorReadingViewSet, IrrigationEventViewSet

router = DefaultRouter()
router.register(r"readings", SensorReadingViewSet, basename="readings")
router.register(r"irrigation-events", IrrigationEventViewSet, basename="irrigation-events")

urlpatterns = [
    path("", include(router.urls)),
]
