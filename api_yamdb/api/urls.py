from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.urls import include, path

from .views import GenreViewSet


app_name = 'api'
router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
urlpatterns = [
    path('v1/', include(router.urls)),
]