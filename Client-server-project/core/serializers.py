from rest_framework import serializers
from .models import Resource, Booking


class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Resource
    fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
  resource_name = serializers.ReadOnlyField(source='resource.name')
  username = serializers.ReadOnlyField(source='user.username')

  class Meta:
    model = Booking
    fields = [
        'id',
        'resource',
        'resource_name',
        'user',
        'username',
        'start_time',
        'end_time',
        'status',
        'created_at',
    ]