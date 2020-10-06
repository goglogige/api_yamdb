from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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
    description = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['author', 'title']


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField("Дата комментария", auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return self.text

