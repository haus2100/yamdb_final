from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    today = timezone.now()
    if value < 0:
        raise ValidationError('Нельзя указывать год меньше "0"')
    if value > today.year:
        raise ValidationError('Нельзя указывать год больше текущего')
    return value
