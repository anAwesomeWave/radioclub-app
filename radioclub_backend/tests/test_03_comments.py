from http import HTTPStatus

import pytest

from songs.models import Song, CommentSong


@pytest.mark.django_db(transaction=False)
class TestComments:
    SONGS_URL = '/api/v1/songs/'

    @staticmethod
    def set_up(user1_client, user1, comments=1, number_songs=1):

        """        default_user = CustomUser.objects.create(
            username='TestUser-1',
            email='testuser1@rclub.fake',
            password='1234567',
            role='Default',
            bio='user1 bio',
        )"""

        song_comments = []

        for i in range(number_songs):
            Song.objects.create(
                name=f'test_song_{i + 1}',
                description='test_description',
                audio_file='http://127.0.0.1:8000/img/name1',
                slug=f'song{i + 1}'
            )
            song_comments.append((i, comments))

        for i in range(number_songs):
            for j in range(song_comments[i][1]):
                CommentSong.objects.create(song_relation_id=i + 1,
                                           text=f'text{j + 1}',
                                           author=user1,
                                           is_visible=(j % 2 == 0),
                                           is_updated=False,
                                           reply_to_id=None
                                           )

    def test_song_comments_page(self, client, user1_client, user1):
        """
            Test existence of list songs page
        """
        self.set_up(user1_client, user1, comments=1, number_songs=1)
        response = client.get(self.SONGS_URL + 'song1/comments/')

        assert response.status_code != HTTPStatus.NOT_FOUND
        assert response.status_code != HTTPStatus.UNAUTHORIZED
        assert response.status_code == HTTPStatus.OK

    def test_is_visible_field_for_song_comments(self, client, admin_client,
                                                moderator_client, user1_client,
                                                user1):
        """
            Test existence of list songs page
            First assert check if objects with is_visible=0 are not displayed
            Second assert check if owner can delete his own comment
            Third assert check if admin can delete any comment
            Fourth assert check if moderator can delete any comment
        """
        self.set_up(user1_client, user1, comments=6, number_songs=1)
        response = client.get(self.SONGS_URL + 'song1/comments/')

        assert 3 == len(response.json())

        user1_client.delete(self.SONGS_URL + 'song1/comments/1/')
        response_owner = client.get(self.SONGS_URL + 'song1/comments/')

        assert 2 == len(response_owner.json())

        admin_client.delete(self.SONGS_URL + 'song1/comments/3/')
        response_admin = client.get(self.SONGS_URL + 'song1/comments/')

        assert 1 == len(response_admin.json())

        moderator_client.delete(self.SONGS_URL + 'song1/comments/5/')
        response_moderator = client.get(self.SONGS_URL + 'song1/comments/')

        assert 0 == len(response_moderator.json())
