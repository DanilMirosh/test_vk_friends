import pytest
from typing import Tuple

from django.test import Client

from users import models as user_models
from friendship import models as friendship_models

from .data_samples import USERS


class FixtureUtils:
    def create_user(user_dict: dict) -> user_models.User:
        new_user = user_models.User.objects.create_user(
            username=user_dict.get('username'),
            password=user_dict.get('password')
        )
        return new_user

    def create_friendship_request(user_from, user_to):
        new_friendship = friendship_models.Friendship.objects.create(
            user_from=user_from, user_to=user_to
        )
        return new_friendship


@pytest.fixture()
def client() -> Client:
    """
    Получаем клиент
    """
    return Client()


@pytest.fixture()
def user1() -> Tuple[dict, user_models.User]:
    """
    Получаем данные первого юзера и его экземпляр в бд
    """
    user = USERS[0]
    new_user = FixtureUtils.create_user(user)
    return (user, new_user)


@pytest.fixture()
def user1_token(client, user1) -> str:
    """
    Получаем токен первого тест юзера
    """
    payload = user1[0]

    response = client.post('/api/v1/auth/login', payload)
    return response.json().get('access_token')


@pytest.fixture()
def auth_client_user1(client, user1_token) -> Client:
    """
    Получаем тест клиент с авторизованным первым юзером
    """
    client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + user1_token
    return client


@pytest.fixture()
def user2() -> Tuple[dict, user_models.User]:
    """
    Получаем данные второго юзера и его экземпляр в бд
    """
    user = USERS[1]
    new_user = FixtureUtils.create_user(user)
    return (user, new_user)


@pytest.fixture()
def user2_token(client, user2) -> str:
    """
    Получаем токен второго тест юзера
    """
    payload = user2[0]

    response = client.post('/api/v1/auth/login', payload)
    return response.json().get('access_token')


@pytest.fixture()
def user3() -> Tuple[dict, user_models.User]:
    """
    Получаем данные третьего юзера и его экземпляр в бд
    """
    user = USERS[2]
    new_user = FixtureUtils.create_user(user)
    return (user, new_user)


@pytest.fixture()
def user4() -> Tuple[dict, user_models.User]:
    """
    Получаем данные четвёртого юзера и его экземпляр в бд
    """
    user = USERS[3]
    new_user = FixtureUtils.create_user(user)
    return (user, new_user)


@pytest.fixture()
def user5() -> Tuple[dict, user_models.User]:
    """
    Получаем данные пятого юзера и его экземпляр в бд
    """
    user = USERS[4]
    new_user = FixtureUtils.create_user(user)
    return (user, new_user)


@pytest.fixture()
def friendship_req_u1_u2(user1, user2) -> friendship_models.Friendship:
    friendship = FixtureUtils.create_friendship_request(user1[1], user2[1])
    return friendship


@pytest.fixture()
def friendship_req_u2_u1(user1, user2) -> friendship_models.Friendship:
    friendship = FixtureUtils.create_friendship_request(user2[1], user1[1])
    return friendship


@pytest.fixture()
def friendship_req_u1_u3(user1, user3) -> friendship_models.Friendship:
    friendship = FixtureUtils.create_friendship_request(user1[1], user3[1])
    return friendship


@pytest.fixture()
def friendship_req_u4_u1(user4, user1) -> friendship_models.Friendship:
    friendship = FixtureUtils.create_friendship_request(user4[1], user1[1])
    return friendship
