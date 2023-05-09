from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router

from auth.jwt import AuthBearer
from auth.schemas import Message

from users.models import User
from users.schemas import UserSchema
from .schemas import FriendshipStatusSchema, FriendshipRequestsSchema

from . import services


friends = Router(tags=["friends"])


@friends.get('/myfriends', auth=AuthBearer(), response={200: Optional[List[UserSchema]], 401: Message})
def get_my_friends(request):
    """
    Получить список своих друзей
    """
    user = request.auth
    return services.get_friends(user)


@friends.get('/requests', auth=AuthBearer(), response={200: FriendshipRequestsSchema, 401: Message},
             summary="Get Incoming And Outgoing Requests")
def get_requests(request):
    """
    Получить входящие и исходящие заявки
    """
    user = request.auth
    incoming = services.get_incoming_requests(user)
    outgoing = services.get_outgoing_requests(user)
    return FriendshipRequestsSchema(incoming=incoming, outgoing=outgoing)


@friends.get('/{user_id}/all', response=List[UserSchema],
             summary="Get User's Friends By His Id")
def get_user_friends_by_id(request, user_id):
    """
    Получить друзей пользователя user_id
    """
    user = get_object_or_404(User, id=user_id)
    return services.get_friends(user)


@friends.get('/{user_id}/status', auth=AuthBearer(),
             response={200: FriendshipStatusSchema, 401: Message, 404: Message},
             summary="Get Friendship Status With Another User By His Id")
def get_friendship_status_by_id(request, user_id):
    """
    Получить статус дружбы с пользователем user_id
    """
    user_from = request.auth
    user_to = get_object_or_404(User, id=user_id)
    status = services.get_friendship_status(user_from, user_to)
    return FriendshipStatusSchema(status=status)


@friends.post('/{user_id}/add', auth=AuthBearer(),
              response={200: Message, 400: Message, 401: Message, 404: Message})
def add_friend_by_id(request, user_id):
    """
    Добавить пользователя user_id в друзья
    """
    user_from = request.auth
    user_to = get_object_or_404(User, id=user_id)
    if user_from.id == user_to.id:
        return 400, {"detail": "Nah you can't add yourself in friends"}
    services.add_to_friends(user_from, user_to)
    return 200, {"detail": "ok"}


@friends.post('/{user_id}/remove', auth=AuthBearer(), response={200: Message, 404: Message})
def remove_friend_by_id(request, user_id):
    """
    Удалить пользователя user_id из друзей/отменить исходящую заявку в друзья.
    """
    user_from = request.auth
    user_to = get_object_or_404(User, id=user_id)
    if not services.remove_from_friends(user_from, user_to):
        return 404, {"detail": "This user is not in friends and you have no outgoing request to him"}
    return 200, {"detail": "ok"}
