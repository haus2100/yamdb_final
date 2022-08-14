from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator'),
)


class User(AbstractUser):
    email = models.EmailField(
        'Email Address',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        blank=True,
        default='user'
    )
