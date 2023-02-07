from django_filters.rest_framework.filterset import FilterSet
from django_filters.filters import Filter

from reviews.models import Title


class TitleFilterSet(FilterSet):
    """Переименовывает поля фильтрации для связанных моделей в Title."""
    category = Filter(field_name='category__slug')
    genre = Filter(field_name='genre__slug')
    name = Filter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ['year', 'category', 'genre', 'name']
