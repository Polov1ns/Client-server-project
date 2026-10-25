from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ResourceViewSet, health_check

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('', include(router.urls)),
]