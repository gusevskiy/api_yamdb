# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def Is_user(self):
        return self.role == "user"


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


# id,title_id,text,author,score,pub_date
class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField()
    score = models.IntegerField(
        verbose_name='Оценка',
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


# id,review_id,text,author,pub_date
class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью',
        unique=False
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.author
