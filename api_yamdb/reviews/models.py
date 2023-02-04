#from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from .validators import year_title


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


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


# id,name,year,category
class Title(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=(year_title, ),
        verbose_name='Дата'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='titles',
    )
    description = models.TextField(
        max_length=255,
        null=True,
        verbose_name='Описание'
        )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр',
        through='GenreTitle'
    )
    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    
    def __str_(self):
        return f'{self.genre} {self.title}'





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

    def __str__(self):
        return self.text


# id,review_id,text,author,pub_date
class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью'
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