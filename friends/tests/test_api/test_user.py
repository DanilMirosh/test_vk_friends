import pytest
from uuid import uuid4


class TestUserApi:
    @pytest.mark.django_db
    def test_get_all_users(self, client, user1, user2):
        users = [user1, user2]
        usernames = [x[0].get('username') for x in users]
        response = client.get('/api/v1/users')

        assert response.status_code == 200
        assert len(response.json()) == 2
        for userdata in response.json():
            assert userdata.get('username') in usernames

    @pytest.mark.django_db
    def test_get_specific_user_by_id(self, client, user1):
        user_data, user_in_db = user1
        user_id = str(user_in_db.id)

        response = client.get('/api/v1/users/id/' + user_id)
        assert response.status_code == 200
        assert response.json().get('id') == user_id
        assert response.json().get('username') == user_data.get('username')

    @pytest.mark.django_db
    def test_get_specific_user_by_nickname(self, client, user1):
        user_data, user_in_db = user1
        username = str(user_in_db.username)

        response = client.get('/api/v1/users/' + username)
        assert response.status_code == 200
        assert response.json().get('id') == str(user_in_db.id)
        assert response.json().get('username') == user_data.get('username')

    @pytest.mark.django_db
    def test_get_user_by_random_uuid(self, client):
        user_id = str(uuid4())

        response = client.get('/api/v1/users/id/' + user_id)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_user_by_random_nickname(self, client):
        username = "amogusamogussugoma"

        response = client.get('/api/v1/users/' + username)
        assert response.status_code == 404
