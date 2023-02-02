from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from .views import (
    GenreViewSet,
    UsersViewSet,
    CategoryViewSet,
    TitleViewSet,
    ReviewViewSet
)


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('review', ReviewViewSet, basename='review')
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', views.signup),
    path('api/v1/auth/token/', views.get_token)
]


"""app_name = 'api'
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
]"""
