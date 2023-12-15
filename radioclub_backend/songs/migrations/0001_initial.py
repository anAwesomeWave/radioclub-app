# Generated by Django 4.2.6 on 2023-12-11 16:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(null=True, upload_to='songs/album-covers/')),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, null=True)),
                ('published_year', models.PositiveSmallIntegerField()),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlbumRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Rating')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommentSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_visible', models.BooleanField(default=True)),
                ('is_updated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, null=True)),
                ('audio_file', models.FileField(null=True, upload_to='songs/song-files/')),
                ('slug', models.SlugField(unique=True)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='songs.album')),
            ],
        ),
        migrations.CreateModel(
            name='SongRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Rating')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_ratings', to='songs.song')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
