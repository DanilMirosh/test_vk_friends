from django.urls import path
from . import views

urlpatterns = [
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('friends/', views.friends, name='friends'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
]