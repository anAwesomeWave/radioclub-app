from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()


class UpdateProfile(serializers.ModelSerializer):
    """ for 'users/me' endpoint """
    avatar = Base64ImageField(required=False, allow_null=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'avatar',
            'bio',
            'username',
            'first_name',
            'last_name',
            'is_superuser',
        )
        read_only_fields = ('is_superuser',)


class UserProfile(serializers.ModelSerializer):
    """Allows users to watch others' profiles."""
    avatar = Base64ImageField(required=False, allow_null=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'avatar',
            'username',
            'bio',
            'first_name',
            'last_name',
            'role',
            'is_superuser',
        )
