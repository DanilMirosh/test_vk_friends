import pytest
from freezegun import freeze_time
from datetime import datetime, timedelta

from users import models as user_models
from friends.settings import JWT_LIVE_TIME_MINUTES


class TestAuthApi:
    @pytest.mark.django_db
    def test_register(self, client):
        data = {'username': 'registertestusername2', 'password': 'amogus11'}
        response = client.post('/api/v1/auth/register', data)
        assert response.status_code == 200

        data = {'username': 'registertestusername2', 'password': 'amogus12'}
        response = client.post('/api/v1/auth/register', data)
        assert response.status_code == 409

    @pytest.mark.django_db
    def test_reg_and_login(self, client):
        data = {'username': 'registertestusername2', 'password': 'amogus11'}
        response = client.post('/api/v1/auth/register', data)
        assert response.status_code == 200

        new_id = response.json().get('id')
        new_object = user_models.User.objects.filter(username=data.get('username')).get()
        assert new_id == str(new_object.id)

        response = client.post('/api/v1/auth/login', data)
        assert response.status_code == 200

        token = response.json().get('access_token')
        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = client.get('/api/v1/auth/whoami', **header)
        assert response.status_code == 200
        assert response.json().get('username') == data.get('username')

    @pytest.mark.django_db
    def test_whoami(self, auth_client_user1, user1):
        response = auth_client_user1.get('/api/v1/auth/whoami')
        assert response.status_code == 200
        assert response.json().get('username') == user1[0].get('username')
        assert response.json().get('id') == str(user1[1].id)

    @pytest.mark.django_db
    def test_whoami_unauthorized(self, client):
        response = client.get('/api/v1/auth/whoami')
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_token_expire(self, client, user1):
        test_date = "2010-01-11T02:23:34+00:00"
        user_data, _ = user1
        with freeze_time(test_date):
            response = client.post('/api/v1/auth/login', user_data)
            token = response.json().get('access_token')
            header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
            response = client.get('/api/v1/auth/whoami', **header)
            assert response.status_code == 200

        with freeze_time(
            datetime.fromisoformat(test_date) + timedelta(seconds=JWT_LIVE_TIME_MINUTES * 60 - 1)
        ):
            response = client.get('/api/v1/auth/whoami', **header)
            assert response.status_code == 200

        with freeze_time(
            datetime.fromisoformat(test_date) + timedelta(minutes=JWT_LIVE_TIME_MINUTES, seconds=1)
        ):
            response = client.get('/api/v1/auth/whoami', **header)
            assert response.status_code == 401
