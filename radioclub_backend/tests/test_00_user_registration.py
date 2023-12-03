from http import HTTPStatus

from django.core import mail
from django.forms.models import model_to_dict
import pytest


@pytest.mark.django_db(transaction=True)
class Test01UsersRegistration:
    URL_SIGNUP = '/api/v1/auth/users/'

    def test_01_nodata_signup(self, client):
        response = client.post(self.URL_SIGNUP)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'''Проверьте, что эндпоинт {self.URL_SIGNUP} доступен.'''
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос, отправленный на эндпоинт `{self.URL_SIGNUP}`, '
            'не содержит необходимых данных, должен вернуться ответ со '
            'статусом 400.'
        )

        response_json = response.json()
        empty_fields = ['email', 'username', 'password']
        for field in empty_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в POST-запросе к `{self.URL_SIGNUP}` не переданы '
                'необходимые данные, в ответе должна возвращаться информация '
                'об обязательных для заполнения полях.'
            )

    def test_01_invalid_data_signup(self, client, django_user_model):
        invalid_data = {
            'email': 'invalid_email',
            'username': ' '
        }
        count_init = django_user_model.objects.count()
        response = client.post(self.URL_SIGNUP, data=invalid_data)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к эндпоинту `{self.URL_SIGNUP}` содержит '
            'некорректные данные, должен вернуться ответ со статусом 400.'
        )
        assert count_init == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}` с '
            'некорректными данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        invalid_fields = ['email', 'username', 'password']
        for field in invalid_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{self.URL_SIGNUP}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

        valid_email = 'validemail@rclub.fake'
        invalid_data = {
            'email': valid_email,
        }
        response = client.post(self.URL_SIGNUP, data=invalid_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к `{self.URL_SIGNUP}` не содержит '
            'данных о `username`, должен вернуться ответ со статусом 400.'
        )
        assert count_init == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}`, не содержащий '
            'данных о `username`, не создаёт нового пользователя.'
        )

        invalid_username = '!#$ewqw*&'
        invalid_data = {
            'email': valid_email,
            'username': invalid_username,
            'password': '123Q3Wd'
        }
        response = client.post(self.URL_SIGNUP, data=invalid_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к `{self.URL_SIGNUP}` содержит'
            'некорректный username, должен вернуться ответ со статусом 400.'
        )

        assert count_init == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}`, содержащий '
            'некорректные данные о `username`, не создаёт нового пользователя.'
        )
        assert ('username' in response.json()
                and isinstance(response.json().get('username'), list)), (
            f'Если в  POST-запросе к `{self.URL_SIGNUP}` переданы '
            'некорректные данные, в ответе должна возвращаться информация '
            'о неправильно заполненных полях.'
        )

    def test_01_valid_user_signup(self, client, django_user_model):
        outbox_before_count = len(mail.outbox)
        valid_data = {
            'email': 'valid@rclub.fake',
            'username': 'valid_username',
            'password': '1Valid23PassWoRd',
        }

        response = client.post(self.URL_SIGNUP, data=valid_data)
        outbox_after = mail.outbox

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.CREATED, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.URL_SIGNUP}`, должен вернуть ответ со статусом 200.'
        )

        new_user = django_user_model.objects.filter(email=valid_data['email'])
        assert new_user.exists(), (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.URL_SIGNUP}`, должен создать нового пользователя.'
        )
        assert new_user.get(email=valid_data['email']).is_active is False, (
            '''Проверьте, что вновь зарегестрированный пользователь не 
            является активным.
            '''
        )
        # Test confirmation code
        assert len(outbox_after) == outbox_before_count + 1, (
            f'Если POST-запрос, отправленный на эндпоинт `{self.URL_SIGNUP}`, '
            f'содержит корректные данные - должен быть отправлен email'
            'с кодом подтвержения.'
        )
        assert valid_data['email'] in outbox_after[0].to, (
            'Если POST-запрос, отправленный на эндпоинт  '
            f'`{self.URL_SIGNUP}`, содержит корректные данные - письмо с '
            'подтверждением должно отправляться на `email`, указанный в '
            'запросе.'
        )

        new_user.delete()
