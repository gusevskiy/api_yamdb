"""from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet"""

from reviews.models import Genre
from .serializers import GenreSerializer
from .mixins import GetPostDeleteViewSet
from .permissions import IsAdminOrReadOnly


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
