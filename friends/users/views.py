from typing import List, Optional
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from .models import User
from .schemas import UserSchema
from auth.schemas import Message


user = Router(tags=["user"])


@user.get('', response=List[UserSchema])
def get_all_users(request):
    """
    Получить всех зарегестрированных пользователей
    """
    return User.objects.all()


@user.get('/{username}', response={200: Optional[UserSchema], 404: Message})
def get_specific_user_by_nickname(request, username: str):
    """
    Получить конкретного пользователя (ник, айди) по нику
    """
    return get_object_or_404(User, username=username)


@user.get('/id/{user_id}', response={200: Optional[UserSchema], 404: Message})
def get_specific_user_by_id(request, user_id: UUID):
    """
    Получить конкретного пользователя (ник, айди) по uuid
    """
    return get_object_or_404(User, id=user_id)
