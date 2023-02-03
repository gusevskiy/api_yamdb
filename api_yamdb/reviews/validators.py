from django.utils import timezone
from django.core.exceptions import ValidationError


def year_title(value):
    year = timezone.now().year
    if value > year:
        raise ValidationError(
            f'{value} не может быть больше {year}'
        )
