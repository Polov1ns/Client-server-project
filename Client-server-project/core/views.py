from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .exceptions import NotFoundError
from .models import Booking, Resource
from .serializers import BookingSerializer, ResourceSerializer


@api_view(['GET'])
def health_check(request):
  return Response({'status': 'ok', 'message': 'System is up and running'})


class ResourceViewSet(viewsets.ModelViewSet):
  queryset = Resource.objects.all()
  serializer_class = ResourceSerializer

  filter_backends = [
      DjangoFilterBackend,
      filters.SearchFilter,
      filters.OrderingFilter,
  ]
  filterset_fields = ['resource_type'] 
  search_fields = [
      'name',
      'description',
  ]
  ordering_fields = ['price_per_hour', 'created_at']  # Сортування


class BookingViewSet(viewsets.ModelViewSet):
  queryset = Booking.objects.select_related('resource', 'user').all()
  serializer_class = BookingSerializer

  # Налаштування фільтрації, пошуку та сортування для Бронювань
  filter_backends = [
      DjangoFilterBackend,
      filters.SearchFilter,
      filters.OrderingFilter,
  ]
  filterset_fields = [
      'status',
      'resource',
      'user',
  ]
  search_fields = [
      'resource__name',
      'user__username',
  ]
  ordering_fields = ['start_time', 'created_at']  # Сортування за часом

  def get_object(self):
    try:
      return super().get_object()
    except (Booking.DoesNotExist, Http404):
      raise NotFoundError('Бронювання з таким ID не знайдено в системі.')