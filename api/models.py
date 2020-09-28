from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=200, null=True)
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
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    def __str__(self):
        return self.text


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
