from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from .views import GenreViewSet, UsersViewSet, CategoryViewSet


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', views.signup),
    path('api/v1/auth/token/', views.get_token)
]
