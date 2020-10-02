from django.db import models


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
