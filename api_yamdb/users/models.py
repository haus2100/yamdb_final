from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254,
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        max_length=9,
        choices=CHOICES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin_access(self):
        return self.is_staff or self.role in (ADMIN, MODERATOR)

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_email_username'
            )
        ]
        ordering = ('id',)

    def __str__(self):
        return self.username
