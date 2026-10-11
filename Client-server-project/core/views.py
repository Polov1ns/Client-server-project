from django.http import Http404
from rest_framework import viewsets
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


class BookingViewSet(viewsets.ModelViewSet):
  queryset = Booking.objects.select_related('resource', 'user').all()
  serializer_class = BookingSerializer

  def get_object(self):
    try:
      return super().get_object()
    except (Booking.DoesNotExist, Http404):
      raise NotFoundError('Бронювання з таким ID не знайдено в системі.')