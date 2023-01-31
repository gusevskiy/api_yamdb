from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# User = get_user_model()

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
    text = models.TimeField()
    score = models.IntegerField(
        verbose_name='Evaluation'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of publication'
    )
    def __str__(self):
        return self.text