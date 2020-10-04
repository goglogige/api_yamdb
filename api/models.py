from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'


class User(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(unique=True, max_length=200, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True, max_length=75)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.user,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
