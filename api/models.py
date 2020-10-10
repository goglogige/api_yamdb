from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    first_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='first name'
    )
    last_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='last name'
    )
    username = models.CharField(
        unique=True,
        max_length=200,
        blank=True,
        verbose_name='username'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='biography'
    )
    email = models.EmailField(
        unique=True,
        max_length=75,
        verbose_name='email'
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='role',
    )

    def __get_user_role(self):
        return self.role

    get_role = property(__get_user_role)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = [F('username').asc(nulls_last=True)]


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
