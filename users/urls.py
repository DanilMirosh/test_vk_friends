from .views import *
from django.urls import path

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_password/', UpdatePasswordView.as_view(), name='update-password'),
    path('friendship/', UserFriendshipView.as_view(), name='friendship'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<str:username>/', FriendRequestDetailView.as_view(), name='friend-request-detail'),
    path('friendship/<str:username>/', FriendshipDetailView.as_view(), name='friendship-detail'),
]
