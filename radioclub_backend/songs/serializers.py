from rest_framework import serializers
from .models import Album, Song, CommentSong, SongRating, \
    AlbumRating


class AlbumListSerializer(serializers.ModelSerializer):
    """List of albums serialize"""
    rating = serializers.IntegerField(
        source='album_ratings__rating__avg',
        read_only=True,
    )

    class Meta:
        model = Album
        fields = (
            'title', 'cover', 'published_year', 'description', 'slug',
            'rating',)


class FilterCommentSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_visible=True)
        return super(FilterCommentSerializer, self).to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

    class Meta:
        model = CommentSong
        list_serializer_class = FilterCommentSerializer


class CommentSongSerializer(serializers.ModelSerializer):
    """Serialize comment structure"""
    replies = RecursiveSerializer(many=True)

    class Meta:
        model = CommentSong
        list_serializer_class = FilterCommentSerializer
        fields = ('text', 'author', 'is_visible', 'is_updated',
                  'created_at', 'song_relation', 'replies')

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.is_visible = validated_data.get('is_visible',
                                                 instance.is_visible)
        instance.is_updated = True
        instance.save()
        return instance


class SongSerializer(serializers.ModelSerializer):
    """Song serializer"""
    album = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Album.objects.all(),
    )
    rating = serializers.IntegerField(
        source='song_ratings__rating__avg',
        read_only=True,
    )

    class Meta:
        model = Song
        fields = (
            'name', 'album', 'description', 'audio_file', 'rating', 'slug')
        read_only_fields = ('audio_file', 'album', 'rating', 'slug')


class AlbumSerializer(serializers.ModelSerializer):
    """List of songs in album serialize"""
    rating = serializers.IntegerField(
        source='album_ratings__rating__avg',
        read_only=True,
    )

    songs = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Song.objects.all(),
        many=True,
    )

    class Meta:
        model = Album
        fields = (
            'title', 'cover', 'published_year', 'description', 'songs',
            'rating')
        required_fields = ('title', 'published_year')
        read_only_fields = ('title', 'songs')

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        album = Album.objects.create(**validated_data)
        for song_data in songs_data:
            Song.objects.create(album=album, **song_data)
        return album

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['songs'] = [
            SongSerializer(song).data for song in instance.songs.all()
        ]
        return representation
