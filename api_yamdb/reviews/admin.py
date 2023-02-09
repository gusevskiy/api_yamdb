from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Comment, Review, Title, Genre, Category, User


User = get_user_model()

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Review)
