#from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
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


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

# id,name,year,category
class Title(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
    )
    year = models.IntegerField(
        validators=(year_title, )
    )
    category = models.ForeignKey(
        Category,
        verbose_name='category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='titles'
    )
    description = models.TextField(
        max_length=255,
        null=True,
        )
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
        verbose_name='жанр'
    )
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name





# id,title_id,text,author,score,pub_date
class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Сomposition'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    text = models.TextField()
    score = models.IntegerField(
        verbose_name='Evaluation',
        default=0,
        validators=[
            MaxLengthValidator(10),
            MinValueValidator(1)
        ],
        
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
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Feedback'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publication'
    )

    def __str__(self):
        return self.text