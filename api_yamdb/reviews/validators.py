import datetime

from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError



def current_year_validator(value):
    value = datetime.date.today().year
    return MaxValueValidator(value)

def validate_year(value):
    if value > datetime.date.today().year:
        raise ValidationError(
            ('%(value)s, год не может быть больше текущего'),
            params={'value': value},
        )
