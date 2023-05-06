from django.urls import path

from users.views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('friend-requests/create/', FriendRequestCreateView.as_view(), name='friend-request-create'),
    path('friend-requests/<int:pk>/respond/', FriendRequestRespondView.as_view(), name='friend-request-respond'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
]
