import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Resource, Booking


class UserDtoSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'roles']

    def get_roles(self, obj):
        return [obj.role.capitalize()]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def validate_password(self, value):
        if not (8 <= len(value) <= 72):
            raise serializers.ValidationError("Password must be between 8 and 72 characters long.")
        if not re.match(r'^[A-Za-z0-9]+$', value):
            raise serializers.ValidationError("Password must contain only Latin letters (A-Z, a-z) and digits (0-9).")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def validate_email(self, value):
        return value.strip().lower()

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data.pop('password')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "An account with this email already exists."})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=validated_data.get('first_name', '').strip(),
            last_name=validated_data.get('last_name', '').strip(),
            role=User.Role.CLIENT
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', '').strip().lower()
        password = data.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        data['user'] = user
        return data


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