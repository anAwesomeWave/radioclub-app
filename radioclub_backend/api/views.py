from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from django.db.models import Avg

from users.serializers import UserProfile
from .permissions import Profile, AdminOrReadOnly
from songs.models import Album, Song
from songs.serializers import AlbumSerializer, AlbumListSerializer, \
    SongSerializer

User = get_user_model()


class SongViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Song.objects.all().annotate(
        Avg('song_ratings__rating')
    )
    serializer_class = SongSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ('get', 'patch')


class AlbumViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    queryset = Album.objects.all().annotate(
        Avg('album_ratings__rating')
    )
    serializer_class = AlbumSerializer
    http_method_names = ('get', 'patch')
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumListSerializer
        return AlbumSerializer


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
    permission_classes = (Profile,)
