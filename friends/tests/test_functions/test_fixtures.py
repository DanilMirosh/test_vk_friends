import pytest

from users import models as user_models
from friendship import models as friendship_models


class TestUserFixtures:
    @pytest.mark.django_db
    def test_user_fixture(self, user1):
        user1_data, user1_in_db = user1
        query = user_models.User.objects.all()

        assert user1_in_db in query
        assert len(query) == 1
        assert user1_data.get('username') == user1_in_db.username

    def friendship_request_exists_from_to(self, user1: user_models.User, user2: user_models.User):
        query = friendship_models.Friendship.objects.filter(user_from=user1, user_to=user2)
        assert len(query) == 1
        assert query.get().user_from == user1
        assert query.get().user_to == user2

    @pytest.mark.django_db
    def test_friendship_fixture1(self, friendship_req_u1_u2, user1, user2):
        _, user1_in_db = user1
        _, user2_in_db = user2
        self.friendship_request_exists_from_to(user1_in_db, user2_in_db)

    @pytest.mark.django_db
    def test_friendship_fixture2(self, friendship_req_u1_u2, friendship_req_u2_u1, user1, user2):
        _, user1_in_db = user1
        _, user2_in_db = user2
        self.friendship_request_exists_from_to(user1_in_db, user2_in_db)

        self.friendship_request_exists_from_to(user2_in_db, user1_in_db)

    @pytest.mark.django_db
    def test_friendship_fixture3(self, friendship_req_u1_u3, friendship_req_u4_u1, user1, user3, user4):
        _, user1_in_db = user1
        _, user3_in_db = user3
        _, user4_in_db = user4
        self.friendship_request_exists_from_to(user1_in_db, user3_in_db)
        self.friendship_request_exists_from_to(user4_in_db, user1_in_db)
