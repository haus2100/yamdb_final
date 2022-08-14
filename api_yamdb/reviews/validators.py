import datetime

from django.core.validators import MaxValueValidator


def current_year_validator(value):
    value = datetime.date.today().year
    return MaxValueValidator(value)
