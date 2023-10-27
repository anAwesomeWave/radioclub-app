from django.db import models


class Album(models.Model):
    cover = models.ImageField(upload_to='covers/')
    title = models.CharField(max_length=30)
    #author = models.ForeignKey(User, on_delete=models.CASCADE())


class Song(models.Model):
    name = models.CharField(max_length=30)
    album = models.ForeignKey(Album, on_delete=models.CASCADE(), related_name='songs')
    audio_file = models.FileField(upload_to='songs/')


class Comment(models.Model):
    text = models.TextField()
    song_relation = models.ForeignKey(Song, on_delete=models.CASCADE(), related_name='comments')
    #author = models.ForeignKey(User, on_delete=models.CASCADE())
