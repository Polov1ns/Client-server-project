from rest_framework import serializers
from .models import Resource, Booking


class ResourceSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = [
            'id',
            'name',
            'resource_type',
            'description',
            'price_per_hour',
            'photo_url',
            'cover_image',
            'cover_image_url',
            'created_at',
        ]
        read_only_fields = ['cover_image']

    def get_cover_image_url(self, obj):
        if not obj.cover_image:
            return None
        return f"/api/resources/{obj.id}/cover/"


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