from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Friendship
from .serializers import FriendshipSerializer

User = get_user_model()


class FriendshipViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.friendship = Friendship.objects.create(from_user=self.user1, to_user=self.user2)

    def test_list_user_friends(self):
        """Тестирование получения списка друзей пользователя"""
        url = reverse('user-friendship-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['to_user']['username'], 'testuser2')

    def test_create_friend_request(self):
        """Тестирование создания заявки в друзья"""
        url = reverse('friend-request-list')
        self.client.force_authenticate(user=self.user1)
        data = {'to_user': 'testuser2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 2)

    def test_create_friend_request_with_invalid_data(self):
        """Тестирование создания заявки в друзья с неправильными данными"""
        url = reverse('friend-request-list')
        self.client.force_authenticate(user=self.user1)
        data = {'to_user': 'testuser1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_accept_friend_request(self):
        """Тестирование принятия заявки в друзья"""
        url = reverse('friend-request-detail', kwargs={'username': 'testuser1'})
        self.client.force_authenticate(user=self.user2)
        data = {'status': Friendship.STATUS_CHOICES[1]}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.friendship.refresh_from_db()
        self.assertEqual(self.friendship.status, Friendship.STATUS_CHOICES[1])

    def test_accept_already_friends(self):
        """Тестирование принятия заявки в друзья, если пользователи уже друзья"""
        friendship = Friendship.objects.create(from_user=self.user1, to_user=self.user2,
                                               status=Friendship.STATUS_CHOICES[1])
        url = reverse('friend-request-detail', kwargs={'username': 'testuser1'})
        self.client.force_authenticate(user=self.user2)
        data = {'status': Friendship.STATUS_CHOICES[1]}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
