from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


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


USER_LEVELS = (
    ("user", "User"),
    ("moderator", "Moderator"),
    ("admin", "Admin")
)


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        # validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


# id,title_id,text,author,score,pub_date
class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Сomposition'
    )
    author = models.IntegerField(
        # 'User',
        # on_delete=models.CASCADE,
        # related_name='reviews',
        verbose_name='Author'
    )
    text = models.TextField()
    score = models.IntegerField(
        verbose_name='Evaluation'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publication'
    )

    def __str__(self):
        return self.text


# id,review_id,text,author,pub_date
class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Feedback'
    )
    text = models.TextField()
    author = models.IntegerField(
        # 'User',
        # on_delete=models.CASCADE,
        # related_name='comments',
        # verbose_name='Author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publication'
    )

    def __str__(self):
        return self.text


# id,name,year,category
class Title(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='category',
        null=True,
        blank=True,
    )
    description = models.TextField(
        max_length=255,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name