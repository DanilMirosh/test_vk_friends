import pytest
from django.urls import reverse

from tests.conftest import UserFactory, FriendshipFactory
from users.models import User
from users.serializers import UserFriendshipSerializer


@pytest.mark.django_db
# @pytest.mark.skip
def test_sign_up(client):
    """Тест на проверку регистрации пользователя"""
    user_data = {
        'username': 'test',
        'first_name': 'test',
        'password': 'test12234567',
        'password_repeat': 'test12234567'
    }

    create_user_response = client.post(
        '/users/signup/',
        data=user_data,
        content_type='application/json')

    user = User.objects.filter(username=user_data['username']).first()

    assert create_user_response.status_code == 201
    assert user.username == user_data['username']


@pytest.mark.django_db
# @pytest.mark.skip
def test_login(client):
    """Тест на проверку входа (login) пользователя"""
    user_data = {
        'username': 'test',
        'password': 'test12234567',
        'password_repeat': 'test12234567'
    }

    create_user_response = client.post(
        '/users/signup/',
        data=user_data,
        content_type='application/json')

    login_user_response = client.post(
        '/users/login/',
        {'username': user_data['username'], 'password': user_data['password']},
        content_type='application/json')

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 200


@pytest.mark.django_db
# @pytest.mark.skip
def test_update_password(client):
    """Тест на проверку смены пароля пользователя"""
    user_data = {
        'username': 'test',
        'password': 'test12234567',
        'password_repeat': 'test12234567'
    }

    create_user_response = client.post(
        '/users/signup/',
        data=user_data,
        content_type='application/json')

    login_user_response = client.post(
        '/users/login/',
        {'username': 'test', 'password': 'test12234567'},
        content_type='application/json')

    new_password = 'testtesttest'

    update_password_response = client.put(
        '/users/update_password/',
        {'old_password': user_data['password'], 'new_password': new_password},
        content_type='application/json')

    login_response = client.post(
        '/users/login/',
        {'username': 'test', 'password': new_password},
        content_type='application/json')

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 200
    assert update_password_response.status_code == 200
    assert login_response.status_code == 200


@pytest.mark.django_db
def test_update_user_profile(client):
    """Тест на проверку редактирования пользователя"""
    user_data = {
        'username': 'test',
        'password': 'test12234567',
        'password_repeat': 'test12234567'
    }

    create_user_response = client.post(
        '/users/signup/',
        data=user_data,
        content_type='application/json'
    )

    login_user_response = client.post(
        '/users/login/',
        {'username': user_data['username'], 'password': user_data['password']},
        content_type='application/json'
    )

    update_user_response = client.patch(
        '/users/profile/', {'username': 'new_test'},
        content_type='application/json'
    )

    user_after_update = User.objects.get(username='new_test')

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 200
    assert login_user_response.data.get('username') == user_data['username']
    assert update_user_response.status_code == 200
    assert user_after_update.username == 'new_test'


@pytest.mark.django_db
# @pytest.mark.skip
def test_delete_user(client):
    """Тест на проверку удаления пользователя"""
    user_data = {
        'username': 'est',
        'password': 'test12234567',
        'password_repeat': 'test12234567'
    }

    create_user_response = client.post(
        '/users/signup/',
        data=user_data,
        content_type='application/json')

    login_user_response = client.post(
        '/users/login/',
        {'username': 'test', 'password': 'test12234567'},
        content_type='application/json')

    user_delete_response = client.delete(
        '/users/profile/',
    )

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 403
    assert user_delete_response.status_code == 403


@pytest.mark.django_db
def test_user_friendship_view_returns_accepted_friendships(client_with_user_logged_in, two_accepted_friendships):
    """Тест на проверку представления UserFriendshipView."""
    user, friend1, friend2 = two_accepted_friendships
    response = client_with_user_logged_in.get(reverse('friendship'))
    assert response.status_code == 200
    assert len(response.data) == 2
    serializer = UserFriendshipSerializer(instance=response.data, many=True)
    assert serializer.data == [
        {"friend": friend1.username},
        {"friend": friend2.username},
    ]

@pytest.mark.django_db
def test_user_factory_creates_users():
    """Тест на проверку UserFactory."""
    user1 = UserFactory()
    user2 = UserFactory()
    assert user1.id != user2.id


@pytest.mark.django_db
def test_friendship_factory_creates_friendships():
    """Тест на проверку FriendshipFactory."""
    user1 = UserFactory()
    user2 = UserFactory()
    friendship1 = FriendshipFactory(from_user=user1, to_user=user2, status='accepted')
    friendship2 = FriendshipFactory(from_user=user2, to_user=user1, status='accepted')
    assert friendship1.id != friendship2.id



