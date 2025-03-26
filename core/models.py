from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('default', 'Default'),
        ('admin', 'Admin'),
    ]
    
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='default')
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Ride(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('en-route', 'En-Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
    ]

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='en-route')
    id_rider = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rider')
    id_driver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='driver')
    pickup_latitude = models.DecimalField(decimal_places=7, max_digits=12, null=True)
    pickup_longitude = models.DecimalField(decimal_places=7, max_digits=12, null=True)
    dropoff_latitude = models.DecimalField(decimal_places=7, max_digits=12, null=True)
    dropoff_longitude = models.DecimalField(decimal_places=7, max_digits=12, null=True)
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"{self.pickup_latitude},{self.pickup_longitude}"


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    description = models.CharField(max_length=512)

    created_at = models.DateTimeField(auto_now_add=True)

