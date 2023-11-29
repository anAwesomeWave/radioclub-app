from http import HTTPStatus

from django.forms.models import model_to_dict
import pytest


@pytest.mark.django_db(transaction=True)
class Test01UserAPI:
    USERS_URL = '/api/v1/users/'
    ME_URL = '/auth/users/me/'
    PATCH_DATA = {
        'first_name': 'changed_name',
        'username': 'changed_uname',
        'last_name': 'changed_lname'
    }

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

    def test_users_page_availability(self, client, user1):
        """ Check that user's page available for everyone """
        url = self.USERS_URL + str(user1.id) + '/'
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

    def test_anonymous_cannot_update_profile(self,
                                             client,
                                             user1,
                                             django_user_model):
        user_id = user1.id
        user_init_data = model_to_dict(
            django_user_model.objects.get(id=user_id)
        )
        url = self.USERS_URL + str(user_id) + '/'
        response = client.patch(url, data=self.PATCH_DATA)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'''Проверьте, что анонимный пользователь получает статус-код
                {HTTPStatus.UNAUTHORIZED}
            '''
        )

        user_data = model_to_dict(django_user_model.objects.get(id=user_id))
        assert user_data == user_init_data, (
            '''Проверьте, что анонимный йпользователь не может менять 
                чужые данные.
            '''
        )

    # @pytest.mark.django_db
    def test_users_me_get(self, user1_client, user1):
        response = user1_client.get(self.ME_URL)

        assert response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что пользователь получает статус-код 
            {HTTPStatus.OK} при GET запросе к своей странице.
            '''
        )

    def test_users_can_change_own_profile(self, django_user_model, user1,
                                          user1_client):
        user_id = user1.id
        url = self.USERS_URL + str(user_id) + '/'
        response = user1_client.patch(url, data=self.PATCH_DATA)

        assert response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что пользователь получает статус-код
            {HTTPStatus.OK} при PATCH запросе к своей странице.
            '''
        )

        changed_user = django_user_model.objects.get(id=user_id)
        for key in self.PATCH_DATA:
            assert getattr(changed_user, key) == self.PATCH_DATA[key], (
                'Проверьте, что PATCH-запрос пользователя к своему профилю '
                'изменяет данные.'
            )

    def test_users_cannot_change_others_profile(self, user1, user2):
        pass