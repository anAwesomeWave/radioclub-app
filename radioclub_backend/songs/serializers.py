from rest_framework import serializers

from .models import Album, Song, CommentSong, CommentAlbum, SongRating, AlbumRating


class AlbumListSerializer(serializers.ModelSerializer):
    """List of albums serialize"""

    class Meta:
        model = Album
        fields = ('title', 'cover', 'published_year')


class BaseCommentSerializer(serializers.ModelSerializer):
    """Serialize comment structure"""

    class Meta:
        abstract = True
        fields = ('text', 'author', 'is_visible', 'is_updated', 'created_at')

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.is_updated = True
        instance.save()
        return instance


class CommentSongSerializer(BaseCommentSerializer):
    """CommentSong serialize"""

    class Meta(BaseCommentSerializer.Meta):
        model = CommentSong
        fields = BaseCommentSerializer.Meta.fields + ('song_relation', 'reply_to')


class CommentAlbumSerializer(serializers.ModelSerializer):
    """CommentSong serialize"""

    class Meta(BaseCommentSerializer.Meta):
        model = CommentAlbum
        fields = BaseCommentSerializer.Meta.fields + ('album_relation', 'reply_to')


class SongSerializer(serializers.ModelSerializer):
    """Song serialize"""
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('name', 'album', 'description', 'average_rating', 'audio_file')

    def get_average_rating(self, obj):
        return obj.average_rating


class AlbumSerializer(serializers.ModelSerializer):
    """List of songs in album serialize"""

    songs = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Song.objects.all(),
        many=True
    )
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ('title', 'cover', 'published_year', 'description', 'average_rating', 'songs')
        required_fields = ('title', 'published_year')

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        album = Album.objects.create(**validated_data)
        for song_data in songs_data:
            Song.objects.create(album=album, **song_data)
        return album

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['songs'] = [
            SongSerializer(song).data for song in instance.song.all()
        ]
        return representation

    def get_average_rating(self, obj):
        return obj.average_rating
