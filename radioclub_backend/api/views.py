from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from django.db.models import Avg
from rest_framework.generics import get_object_or_404
from users.serializers import UserProfile
from rest_framework import status
from .permissions import Profile, AdminOrReadOnly, IsOwnerOrModerator
from songs.models import Album, Song, CommentSong
from songs.serializers import AlbumSerializer, AlbumListSerializer, \
    SongSerializer, CommentSongSerializer

User = get_user_model()


class CommentSongViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSongSerializer
    permission_classes = (IsOwnerOrModerator,)

    def get_slug(self):
        return get_object_or_404(Song, slug=self.kwargs['slug'])

    def get_queryset(self, **kwargs):
        return self.get_slug().song_comments.filter(reply_to=None)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.is_visible = False
        comment.save()
        data = CommentSongSerializer(comment).data
        return Response(data, status=status.HTTP_200_OK)


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
    mixins.ListModelMixin,
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
