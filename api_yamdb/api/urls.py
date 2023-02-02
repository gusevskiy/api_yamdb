from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from .views import (
    GenreViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    UsersViewSet
)


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('review', ReviewViewSet, basename='review')
router.register('review', CommentViewSet, basename='comment')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/signup/', views.signup),
    path('auth/token/', views.get_token)
]
