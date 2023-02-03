from django.contrib import admin

#from api.models import User
from django.contrib.auth import get_user_model
from .models import Comment, Review, Title, Genre, Category


User = get_user_model()

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)




##### delete
# from django.contrib import admin

# from .models import User

# admin.site.register(User)
