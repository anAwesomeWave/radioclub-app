from rest_framework.test import APIClient
import pytest
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_superuser(django_user_model):
    # https://pytest-django.readthedocs.io/en/latest/helpers.html#django
    # -user-model
    return django_user_model.objects.create_superuser(
        username='TestSuperuser',
        email='testsuperuser@rclub.fake',
        password='1234567',
        bio='superuser bio'
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username='TestAdmin',
        email='testadmin@rclub.fake',
        password='1234567',
        role='Admin',
        bio='admin bio'
    )


@pytest.fixture
def moderator(django_user_model):
    return django_user_model.objects.create_user(
        username='TestModerator',
        email='testmoderator@rclub.fake',
        password='1234567',
        role='Moderator',
        bio='moder bio'
    )


@pytest.fixture
def user1(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser-1',
        email='testuser1@rclub.fake',
        password='1234567',
        role='Default',
        bio='user1 bio',
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser-2',
        email='testuser2@rclub.fake',
        password='1234567',
        role='Default',
        bio='user2 bio'
    )


@pytest.fixture
def token_user_superuser(user_superuser):
    token = AccessToken.for_user(user_superuser)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_superuser_client(token_user_superuser):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token_user_superuser["access"]}'
    )
    return client


@pytest.fixture
def token_admin(admin):
    token = AccessToken.for_user(admin)
    return {
        'access': str(token),
    }


@pytest.fixture
def admin_client(token_admin):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_admin["access"]}')
    return client


@pytest.fixture
def token_moderator(moderator):
    token = AccessToken.for_user(moderator)
    return {
        'access': str(token),
    }


@pytest.fixture
def moderator_client(token_moderator):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token_moderator["access"]}'
    )
    return client


@pytest.fixture
def token_user1(user1):
    token = AccessToken.for_user(user1)
    return {
        'access': str(token),
    }


@pytest.fixture
def user1_client(token_user1):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user1["access"]}')
    return client


@pytest.fixture
def token_user2(user2):
    token = AccessToken.for_user(user2)
    return {
        'access': str(token),
    }


@pytest.fixture
def user2_client(token_user2):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user2["access"]}')
    return client
