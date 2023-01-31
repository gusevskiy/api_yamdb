from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    bio = models.TextField(
    'Биография',
    blank=True,
    )


# id,title_id,text,author,score,pub_date
class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Сomposition'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
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
    author = models.ForeignKey(
        'User',
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
