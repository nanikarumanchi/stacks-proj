from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import UserManager


class GuestEmail(models.Model):
    email = models.EmailField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
