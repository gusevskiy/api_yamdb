from django.db import models
from django.contrib.auth.models import AbstractUser


USER_LEVELS = (
    ("user", "User"),
    ("moderator", "Moderator"),
    ("admin", "Admin")
)


class User(AbstractUser):
    role = models.CharField(
        'role',
        max_length=32,
        choices=USER_LEVELS,
        default="user"
    )
    bio = models.TextField(
        'bio',
        max_length=256,
        blank=True
    )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='category'
    )


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'genre'],
                                    name='unique_title_genre_pair')
        ]
