from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    DEFAULT_USER = 'Default'
    ROLE_CHOICE = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (DEFAULT_USER, DEFAULT_USER),
    ]
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICE,
        default=DEFAULT_USER,
        null=False,
        blank=True
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='users/avatars'
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
