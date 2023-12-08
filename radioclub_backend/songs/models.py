from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Album(models.Model):
    cover = models.ImageField(
        upload_to='songs/album-covers/',
        null=True
    )
    title = models.CharField(
        max_length=60,
        null=False,
        blank=False
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    published_year = models.PositiveSmallIntegerField(
        null=False,
        blank=False
    )
    slug = models.SlugField(
        unique=True
    )


class Song(models.Model):
    name = models.CharField(
        max_length=60,
        null=False,
        blank=False
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='songs',
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    audio_file = models.FileField(
        upload_to='songs/song-files/',
        null=True
    )
    slug = models.SlugField(
        unique=True
    )


class BaseRating(models.Model):
    rating = models.PositiveSmallIntegerField(
        'Rating',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0
    )

    class Meta:
        abstract = True


class AlbumRating(BaseRating):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='album_ratings'
    )


class SongRating(BaseRating):
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='song_ratings'
    )


class CommentSong(models.Model):
    song_relation = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='song_comments'
    )
    text = models.TextField(
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_visible = models.BooleanField(
        null=False,
        default=True
    )
    is_updated = models.BooleanField(
        null=False,
        default=False
    )
    reply_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies',
    )
    created_at = models.DateTimeField()
