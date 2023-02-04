from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from .views import GenreViewSet, UsersViewSet, CategoryViewSet, TitleViewSet


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.signup),
    path('v1/auth/token/', views.get_token)
]
