from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        null=False
    )
    is_banned = models.BooleanField(
        null=False,
        default=False,
    )
    is_moderator = models.BooleanField(
        null=False,
        default=False,
    )
    is_admin = models.BooleanField(
        null=False,
        default=False,
    )
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
