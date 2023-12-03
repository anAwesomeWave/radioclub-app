from http import HTTPStatus

from django.forms.models import model_to_dict
import pytest


@pytest.mark.django_db(transaction=True)
class Test01UserAPI:
    USERS_URL = '/api/v1/users/'
    ME_URL = '/api/v1/auth/users/me/'
    PATCH_DATA = {
        'first_name': 'changed_name',
        'username': 'changed_uname',
        'last_name': 'changed_lname'
    }

    def test_users_list_availability(self, client):
        """Test that page with all users available"""

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
        """Test that anonymous users cannot update other's profiles"""

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

    def test_users_me_get(self, user1_client, client):
        anon_response = client.get(self.ME_URL)
        response = user1_client.get(self.ME_URL)

        assert response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что пользователь получает статус-код 
            {HTTPStatus.OK} при GET запросе к {self.ME_URL}.
            '''
        )

        assert anon_response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'''Проверьте, что анонимный пользователь получает статус-код
            {HTTPStatus.UNAUTHORIZED} При GET запросе к {self.ME_URL}
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

    def test_users_cannot_change_others_profile(self, user1, user2_client,
                                                django_user_model):
        user1_id = user1.id
        user_init_data = model_to_dict(
            django_user_model.objects.get(id=user1_id)
        )
        url = self.USERS_URL + str(user1_id) + '/'
        response = user2_client.patch(url, data=self.PATCH_DATA)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'''Проверьте, что пользователь получает статус-код
                {HTTPStatus.FORBIDDEN}, при попытки изменить чужой профиль.
            '''
        )

        user_data = model_to_dict(django_user_model.objects.get(id=user1_id))
        assert user_data == user_init_data, (
            '''Проверьте, что пользователь не может менять 
                чужые данные.
            '''
        )


@pytest.mark.django_db(transaction=True)
class Test01AdminApi:
    USERS_URL = '/api/v1/users/'
    ME_URL = '/auth/users/me/'
    PATCH_DATA = {
        'first_name': 'changed_name',
        'username': 'changed_uname',
        'last_name': 'changed_lname'
    }
    ADMIN_PATCH_DATA = {
        'role': 'Moderator'
    }

    ADMIN_BAN_DATA = {
        'role': 'Banned'
    }

    def test_admin_can_change_users_roles(self, admin_client, user1,
                                          django_user_model):
        user_id = user1.id
        url = self.USERS_URL + str(user_id) + '/'
        response = admin_client.patch(url, data=self.ADMIN_PATCH_DATA)

        assert response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что админ получает
            {HTTPStatus.OK} при изменении роли пользователя.
            '''
        )

        new_user_role = model_to_dict(
            django_user_model.objects.get(id=user_id)
        )
        assert new_user_role['role'] == self.ADMIN_PATCH_DATA['role'], (
            f'''Проверьте, что PATCH запрос админа к {url} на изменение роли 
                пользователя действительно меняет его роль в бд.
            '''
        )

    def test_admin_cannot_change_other_users_data(self, admin_client, user1,
                                                  django_user_model):
        user_id = user1.id
        url = self.USERS_URL + str(user_id) + '/'
        response = admin_client.patch(url, data=self.ADMIN_PATCH_DATA)

        assert response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что админ получает
            {HTTPStatus.OK} при изменении роли пользователя.
            '''
        )

        new_user_role = model_to_dict(
            django_user_model.objects.get(id=user_id)
        )
        assert new_user_role['role'] == self.ADMIN_PATCH_DATA['role'], (
            f'''Проверьте, что PATCH запрос админа к {url} на изменение роли 
                пользователя действительно меняет его роль в бд.
            '''
        )

    def test_admin_can_change_own_data(self, admin, admin_client,
                                       django_user_model):
        admin_id = admin.id
        url = self.USERS_URL + str(admin_id) + '/'
        response = admin_client.patch(url, data=self.PATCH_DATA)

        assert response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что админ получает статус-код {HTTPStatus.OK} 
            при попытке изменить свои данные
            '''
        )

        changed_admin = django_user_model.objects.get(id=admin_id)
        for key in self.PATCH_DATA:
            assert getattr(changed_admin, key) == self.PATCH_DATA[key], (
                'Проверьте, что PATCH-запрос админа к своему профилю '
                'изменяет данные.'
            )

    def test_moderator(self, moderator_client, user1, django_user_model):
        user_id = user1.id
        url = self.USERS_URL + str(user_id) + '/'
        ban_response = moderator_client.patch(url, data=self.ADMIN_BAN_DATA)

        assert ban_response.status_code == HTTPStatus.OK, (
            f'''Проверьте, что модератор получает
            {HTTPStatus.OK} при попытке забанить пользователя.
            '''
        )
        response = moderator_client.patch(url, data=self.ADMIN_PATCH_DATA)

        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'''Проверьте, что модератор получает
            {HTTPStatus.FORBIDDEN} при изменении роли пользователя на 
            модерскую.
            '''
        )

        new_user_role = model_to_dict(
            django_user_model.objects.get(id=user_id)
        )
        assert new_user_role['role'] == self.ADMIN_BAN_DATA['role'], (
            f'''Проверьте, что PATCH запрос модератора к {url} на изменение 
            роли пользователя на {self.ADMIN_BAN_DATA['role']}
            действительно меняет его роль в бд.
            '''
        )
