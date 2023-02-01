from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views
from .views import GenreViewSet, CategoryViewSet


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/signup/', views.signup),
    path('auth/token/', views.get_token)
]
