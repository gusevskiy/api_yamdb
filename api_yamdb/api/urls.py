from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from .views import GenreViewSet, UsersViewSet


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UsersViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', views.signup),
    path('auth/token/', views.get_token)
]