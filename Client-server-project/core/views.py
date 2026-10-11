from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resource
from .serializers import ResourceSerializer


@api_view(['GET'])
def health_check(request):
  return Response({'status': 'ok', 'message': 'System is up and running'})


class ResourceViewSet(viewsets.ModelViewSet):
  queryset = Resource.objects.all()
  serializer_class = ResourceSerializer