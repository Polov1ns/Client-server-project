from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health_check,
    ResourceViewSet,
    BookingViewSet,
    RegisterView,
    LoginView,
)

router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('', include(router.urls)),
]