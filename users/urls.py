from .views import *
from django.urls import path

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update-password'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('friend_requests/', FriendRequestsView.as_view(), name='friend_requests'),

]
