from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Album(models.Model):
    cover = models.ImageField(upload_to='songs/album-covers/', null=True)
    title = models.CharField(max_length=60, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    published_year = models.PositiveSmallIntegerField()
    slug = models.SlugField(unique=True)


class Song(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    description = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='songs/song-files/', null=True)
    slug = models.SlugField(unique=True)


class CommentSong(models.Model):
    text = models.TextField(null=False, blank=False)
    song_relation = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField()
