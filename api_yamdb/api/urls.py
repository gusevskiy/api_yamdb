from django.urls import path
from . import views


urlpatterns = [
    path('auth/signup/', views.signup),
    path('auth/token/', views.get_token)
]