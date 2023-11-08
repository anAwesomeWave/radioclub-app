from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from users.serializers import UserProfile
from .permissions import Profile

User = get_user_model()


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """ Viewset for viewing user's profile.
        Все пользователи смогут видеть эту страницу, а модераторы править
        что-то, админы также смогут назначать модераторов и других адмминов
        и снимать модеров
    """
    queryset = User.objects.all()
    http_method_names = ('get', 'patch')
    serializer_class = UserProfile
    permission_classes = (Profile, )
