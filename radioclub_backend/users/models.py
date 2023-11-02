from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    DEFAULT_USER = 'Default'
    BANNED_USER = 'Banned'
    ROLE_CHOICE = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (DEFAULT_USER, DEFAULT_USER),
        (BANNED_USER, BANNED_USER),
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
    bio = models.TextField(
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_banned(self):
        return self.role == self.BANNED_USER

    @property
    def is_user(self):
        return self.role == self.DEFAULT_USER

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
