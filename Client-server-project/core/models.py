from django.contrib.auth.models import AbstractUser
from django.db import models


# Кастомна модель користувача
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager/Owner'
        CLIENT = 'client', 'Client'

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.CLIENT
    )


# Сутність Ресурсу (переговорні кімнати, робочі місця, обладнання тощо)
class Resource(models.Model):
    name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(blank=True, null=True)
    cover_image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.resource_type})'


# Сутність Бронювання 
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name='bookings'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'status'], name='idx_booking_time_status'),
        ]

    def __str__(self):
        return (
            f'Booking {self.id}: {self.resource.name} by {self.user.username}'
        )


# Сутність Відгуку
class Review(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='review'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    sentiment_score = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for Booking {self.booking.id} - Rating: {self.rating}'