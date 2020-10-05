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


class Category(models.Model):
    """Категории произведений"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.ManyToManyField(
        Genre,
        related_name="titles_genre",
    )
    category = models.ForeignKey(
        Category, blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles_category"
    )
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name

