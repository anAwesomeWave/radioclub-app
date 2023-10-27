from rest_framework import serializers

from .models import Album, Song, Comment


class AlbumListSerializer(serializers.ModelSerializer):
    """List of albums"""

    class Meta:
        model = Album
        fields = ('title', 'cover')


class AlbumDetailSerializer(serializers.ModelSerializer):
    """List of songs in album"""

    class Meta:

