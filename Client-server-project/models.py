from django.contrib.auth.models import AbstractUser
from django.db import models


# 1. Кастомна модель користувача з ролями відповідно до вимог
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager/Owner"
        CLIENT = "client", "Client"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)


# 2. Сутність Ресурсу (переговорні кімнати, коворкінг, обладнання тощо)
class Resource(models.Model):
    name = models.CharField(max_length=255)
    resource_type = models.CharField(
        max_length=100
    )  # Наприклад: "Conference Room", "Workplace"
    description = models.TextField(blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(
        blank=True, null=True
    )  # Посилання на фото у хмарному сховищі
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.resource_type})"


# 3. Сутність Бронювання
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id}: {self.resource.name} by {self.user.username}"


# 4. Сутність Відгуку (з подальшим аналізом тональності ШІ)
class Review(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="review"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Наприклад, від 1 до 5
    comment = models.TextField(blank=True, null=True)
    sentiment_score = models.CharField(
        max_length=50, blank=True, null=True
    )  # Для результатів ШІ (positive/neutral/negative)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Booking {self.booking.id} - Rating: {self.rating}"

class Resource(models.Model):
    name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(blank=True, null=True)
    cover_image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.resource_type})"