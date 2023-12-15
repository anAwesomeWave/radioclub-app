from http import HTTPStatus

from songs.models import Song
import pytest


@pytest.mark.django_db(transaction=False)
class TestSongs:
    SONGS_URL = '/api/v1/songs/'

    @staticmethod
    def set_up(number_songs=2):
        for i in range(1, number_songs):
            Song.objects.create(
                name=f'test_song_{i}',
                description='test_description',
                audio_file=f'http://127.0.0.1:8000/img/name{i}',
                slug=f'song{i}'
            )

    def test_song_availability(self, client):
        """
            Test existence of song page
        """

        self.set_up()

        response = client.get(self.SONGS_URL + 'song1/')
        assert response.status_code != HTTPStatus.NOT_FOUND
        assert response.status_code != HTTPStatus.UNAUTHORIZED
        assert response.status_code == HTTPStatus.OK

    def test_songs_list_availability(self, client):
        """
            Test existence of list songs page
        """

        response = client.get(self.SONGS_URL)

        assert response.status_code != HTTPStatus.NOT_FOUND
        assert response.status_code != HTTPStatus.UNAUTHORIZED
        assert response.status_code == HTTPStatus.OK

    def test_create_delete_song_objects(self, client):
        """
            Test object's creation
        """

        valid_data = [{'name': 'test_song_1', 'album': None,
                       'description': 'test_description',
                       'audio_file': 'http://testserver/img/http%3A/127.0.0'
                                     '.1%3A8000/img/name1',
                       'rating': None,
                       'slug': 'song1'},
                      {'name': 'test_song_2', 'album': None,
                       'description': 'test_description',
                       'audio_file': 'http://testserver/img/http%3A/127.0.0'
                                     '.1%3A8000/img/name2',
                       'rating': None,
                       'slug': 'song2'},
                      {'name': 'test_song_3', 'album': None,
                       'description': 'test_description',
                       'audio_file': 'http://testserver/img/http%3A/127.0.0'
                                     '.1%3A8000/img/name3',
                       'rating': None,
                       'slug': 'song3'}]

        self.set_up(number_songs=4)
        response = client.get(self.SONGS_URL)
        Song.objects.filter(name='test_song_1').delete()
        response_after_delete = client.get(self.SONGS_URL)
        assert response.json()['results'] == valid_data
        assert response_after_delete.json()['results'] == valid_data[1:]
