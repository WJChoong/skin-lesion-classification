# skin_detection/models.py

from django.db import models
from django.utils import timezone

class User(models.Model):
    id = models.AutoField(primary_key=True)  # Manually added ID field
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True)

class Auth(models.Model):
    id = models.AutoField(primary_key=True)  # Manually added ID field
    password = models.CharField(max_length=128)
    level = models.CharField(max_length=50)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class Image(models.Model):
    id = models.AutoField(primary_key=True)  # Manually added ID field
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)  # Manually added ID field
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True)