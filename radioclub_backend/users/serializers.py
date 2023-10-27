from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()


class UpdateProfile(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name')
