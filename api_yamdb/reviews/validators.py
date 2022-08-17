from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_score(value):
    if value < 0 or value > 10:
        raise ValidationError(
            _('%(value)s не входит в диапазон 0...10'),
            params={'value': value},
        )


def validate_year(value):
    if value > date.today().year:
        raise ValidationError(
            _('%(value)s, год не может быть больше текущего'),
            params={'value': value},
        )
