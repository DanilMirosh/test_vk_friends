import factory
import pytest
from django.contrib.auth import get_user_model

from users.models import Friendship, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    print(f"Created user: {username}")


class FriendshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friendship

    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    status = 'accepted'
    # print(f"Created friendship: {from_user.username} -> {to_user.username}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        from_user = kwargs.get('from_user')
        to_user = kwargs.get('to_user')
        friendship = model_class(from_user=from_user, to_user=to_user, status='accepted')
        friendship.save()
        print(f"Created friendship: {from_user.username} -> {to_user.username}")
        return friendship




@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def friendship_factory():
    return FriendshipFactory


@pytest.fixture
def client_with_user_logged_in(client, user_factory):
    """Фикстура для авторизации пользователя."""
    user = user_factory()
    client.force_login(user)
    return client


@pytest.fixture
def two_accepted_friendships(friendship_factory, user_factory):
    """Фикстура для создания двух принятых дружб."""
    user = user_factory()
    friend1 = user_factory()
    friend2 = user_factory()
    friendship_factory(from_user=user, to_user=friend1, status='accepted').save()
    friendship_factory(from_user=friend2, to_user=user, status='accepted').save()
    return user, friend1, friend2

# @pytest.fixture
# def test_user_friendship_view(client, user_factory, friendship_factory):
#     user = user_factory()
#     friend1 = user_factory()
#     friend2 = user_factory()
#     friendship_factory(from_user=user, to_user=friend1, status='accepted')
#     friendship_factory(from_user=friend2, to_user=user, status='accepted')
