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
