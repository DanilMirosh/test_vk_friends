import pytest

from users import models as user_models
from friendship import (
    schemas as friendship_schemas,
    models as friendship_models
)


class TestFriendshipApi:
    @pytest.mark.django_db
    def test_my_friends_empty(self, auth_client_user1, friendship_req_u1_u3, friendship_req_u4_u1):
        response = auth_client_user1.get('/api/v1/friends/myfriends')
        assert response.status_code == 200
        assert len(response.json()) == 0

    @pytest.mark.django_db
    def test_my_friends(self, auth_client_user1, friendship_req_u1_u2,
                        friendship_req_u2_u1, friendship_req_u1_u3):
        response = auth_client_user1.get('/api/v1/friends/myfriends')
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.django_db
    def test_requests(self, auth_client_user1, friendship_req_u1_u2,
                      friendship_req_u2_u1, friendship_req_u4_u1, friendship_req_u1_u3,
                      user1, user2, user3, user4):
        response = auth_client_user1.get('/api/v1/friends/requests')
        assert response.status_code == 200
        incoming = response.json().get('incoming')
        outgoing = response.json().get('outgoing')
        assert len(incoming) == 1
        assert incoming[0].get('username') == user4[1].username
        assert len(outgoing) == 1
        assert outgoing[0].get('username') == user3[1].username

    @pytest.mark.django_db
    def test_get_users_friends(self, client, user1, user2, user3, user4,
                               friendship_req_u1_u2, friendship_req_u2_u1, friendship_req_u1_u3):
        def check_user_is_only_friend(user2: user_models.User, response):
            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()[0].get('username') == user2.username

        _, user1_in_db = user1
        _, user2_in_db = user2

        response = client.get('/api/v1/friends/' + str(user1_in_db.id) + '/all')
        check_user_is_only_friend(user2_in_db, response)

        response = client.get('/api/v1/friends/' + str(user2_in_db.id) + '/all')
        check_user_is_only_friend(user1_in_db, response)

    @pytest.mark.django_db
    def test_get_friendship_status(self, auth_client_user1, user1, user2, user3, user4, user5,
                                   friendship_req_u1_u2, friendship_req_u2_u1, friendship_req_u1_u3,
                                   friendship_req_u4_u1):
        _, user1_in_db = user1
        _, user2_in_db = user2
        _, user3_in_db = user3
        _, user4_in_db = user4
        _, user5_in_db = user5

        users = (user1_in_db, user2_in_db, user3_in_db, user4_in_db, user5_in_db)

        statuses = (
            friendship_schemas.FriendshipStatus.NONE,
            friendship_schemas.FriendshipStatus.FRIENDS,
            friendship_schemas.FriendshipStatus.OUTGOING,
            friendship_schemas.FriendshipStatus.INCOMING,
            friendship_schemas.FriendshipStatus.NONE
        )

        for user, status in zip(users, statuses):
            response = auth_client_user1.get('/api/v1/friends/' + str(user.id) + '/status')
            assert response.status_code == 200
            assert response.json().get('status') == status

    @pytest.mark.django_db
    def test_add_friend(self, auth_client_user1, user1, user2):
        _, user1_in_db = user1
        _, user2_in_db = user2

        for _ in range(3):
            response = auth_client_user1.post('/api/v1/friends/' + str(user2_in_db.id) + '/add')
            assert response.status_code == 200
        query = friendship_models.Friendship.objects.filter(user_from=user1_in_db, user_to=user2_in_db)
        assert len(query) == 1

        response = auth_client_user1.get('/api/v1/friends/' + str(user2_in_db.id) + '/status')
        assert response.status_code == 200
        assert response.json().get('status') == friendship_schemas.FriendshipStatus.OUTGOING

    @pytest.mark.django_db
    def test_remove_friend(self, auth_client_user1, user1, user2, friendship_req_u2_u1):
        _, user1_in_db = user1
        _, user2_in_db = user2

        response = auth_client_user1.get('/api/v1/friends/' + str(user2_in_db.id) + '/status')
        assert response.status_code == 200
        assert response.json().get('status') == friendship_schemas.FriendshipStatus.INCOMING

        response = auth_client_user1.post('/api/v1/friends/' + str(user2_in_db.id) + '/add')
        assert response.status_code == 200

        response = auth_client_user1.get('/api/v1/friends/' + str(user2_in_db.id) + '/status')
        assert response.status_code == 200
        assert response.json().get('status') == friendship_schemas.FriendshipStatus.FRIENDS

        response = auth_client_user1.post('/api/v1/friends/' + str(user2_in_db.id) + '/remove')
        assert response.status_code == 200

        response = auth_client_user1.get('/api/v1/friends/' + str(user2_in_db.id) + '/status')
        assert response.status_code == 200
        assert response.json().get('status') == friendship_schemas.FriendshipStatus.INCOMING

    @pytest.mark.django_db
    def test_remove_friend_special_case(self, auth_client_user1, client, user2_token, user1, user2,
                                        friendship_req_u2_u1):
        _, user1_in_db = user1
        _, user2_in_db = user2

        response = auth_client_user1.post('/api/v1/friends/' + str(user2_in_db.id) + '/add')
        assert response.status_code == 200

        response = auth_client_user1.get('/api/v1/friends/' + str(user2_in_db.id) + '/status')
        assert response.status_code == 200
        assert response.json().get('status') == friendship_schemas.FriendshipStatus.FRIENDS

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + user2_token}
        response = client.post('/api/v1/friends/' + str(user1_in_db.id) + '/remove', **header)
        assert response.status_code == 200

        response = auth_client_user1.get('/api/v1/friends/' + str(user2_in_db.id) + '/status')
        assert response.status_code == 200
        assert response.json().get('status') == friendship_schemas.FriendshipStatus.NONE
