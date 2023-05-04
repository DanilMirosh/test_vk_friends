from django.urls import path
from .views import register, send_friend_request

urlpatterns = [
    path('register/', register, name='register'),
    path('send_friend_request/<int:friend_id>/', send_friend_request, name='send_friend_request'),
]