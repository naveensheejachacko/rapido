from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class RideStatus(models.TextChoices):
    REQUESTED = 'REQUESTED', 'Requested'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Location(models.Model):
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Ride(models.Model):
    rider = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='rides_as_rider'
    )
    driver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='rides_as_driver'
    )
    pickup_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='rides_from'
    )
    dropoff_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='rides_to'
    )
    status = models.CharField(
        max_length=20,
        choices=RideStatus.choices,
        default=RideStatus.REQUESTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    current_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    vehicle_number = models.CharField(max_length=20, blank=True)
    rating = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
