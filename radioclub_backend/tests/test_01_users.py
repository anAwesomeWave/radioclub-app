from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test01UserAPI:
    USERS_URL = '/api/v1/users/'

    def test_users_list_availability(self, client):
        response = client.get(self.USERS_URL)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Проверьте, что страница {self.USERS_URL} доступна'
        )
        assert response.status_code != HTTPStatus.UNAUTHORIZED, (
            f'''Проверьте, что страница {self.USERS_URL}
            доступна неаутентифицированным пользователям'''
        )
        assert response.status_code == HTTPStatus.OK, (
            f'''
            GET запрос к странице {self.USERS_URL} вернул отличное от
            200 значение ({response.status_code})
            '''
        )

    def test_users_page_availability(self, client, user):
        """ Check that user's page available for everyone """
        url = self.USERS_URL + str(user.id) + '/'
        response = client.get(url)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Проверьте, что страница {url} доступна'
        )
        assert response.status_code != HTTPStatus.UNAUTHORIZED, (
            f'''Проверьте, что страница {url}
            доступна неаутентифицированным пользователям'''
        )
        assert response.status_code == HTTPStatus.OK, (
            f'''
            GET запрос к странице {url} вернул отличное от
            200 значение ({response.status_code})
            '''
        )