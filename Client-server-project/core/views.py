import os
from django.http import FileResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .exceptions import NotFoundError
from .models import Booking, Resource
from .serializers import BookingSerializer, ResourceSerializer
from .services import CoverImageService, InvalidFileUploadException


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'System is up and running'})


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all().order_by('id')
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
    ordering_fields = ['price_per_hour', 'created_at']

    @action(detail=True, methods=['post', 'get', 'delete'], url_path='cover')
    def cover_management(self, request, pk=None):
        resource = self.get_object()

        if request.method == 'GET':
            if not resource.cover_image:
                raise Http404("The cover image for this resource does not exist.")
            file_path = CoverImageService.get_file_path(resource.cover_image)
            if not file_path:
                raise Http404("The cover image file is unavailable.")
            
            ext = os.path.splitext(file_path)[1].lower()
            content_type = 'image/png' if ext == '.png' else 'image/jpeg'
            return FileResponse(open(file_path, 'rb'), content_type=content_type)

        elif request.method == 'POST':
            file_obj = request.FILES.get('cover')
            try:
                CoverImageService.validate_and_save(resource, file_obj)
                serializer = self.get_serializer(resource)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except InvalidFileUploadException as e:
                return Response(
                    {
                        "type": "Invalid cover image",
                        "title": "Bad Request",
                        "status": 400,
                        "detail": str(e),
                        "instance": request.path
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif request.method == 'DELETE':
            if not resource.cover_image:
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            old_cover = resource.cover_image
            resource.cover_image = None
            resource.save()
            CoverImageService.delete_file_by_name(old_cover)
            return Response(status=status.HTTP_204_NO_CONTENT)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = (
        Booking.objects.select_related('resource', 'user').all().order_by('id')
    )
    serializer_class = BookingSerializer

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
    ordering_fields = ['start_time', 'created_at']

    def get_object(self):
        try:
            return super().get_object()
        except (Booking.DoesNotExist, Http404):
            raise NotFoundError('Бронювання з таким ID не знайдено в системі.')