from typing import Tuple, List

from users.models import User
from .schemas import FriendshipStatus
from .models import Friendship


def get_friendship_status(user_from: User, user_to: User) -> FriendshipStatus:
    """
    Получить статус дружбы между двумя пользователями.
    """
    status = FriendshipStatus.NONE
    exists_outgoing = Friendship.objects.filter(user_from=user_from, user_to=user_to).exists()
    exists_incoming = Friendship.objects.filter(user_from=user_to, user_to=user_from).exists()
    if exists_incoming and exists_outgoing:
        status = FriendshipStatus.FRIENDS
    elif exists_outgoing:
        status = FriendshipStatus.OUTGOING
    elif exists_incoming:
        status = FriendshipStatus.INCOMING

    return status


def add_to_friends(user_from: User, user_to: User) -> None:
    """
    Добавить пользователя в друзья. Если заявка уже есть, то ничего не произойдёт.
    """
    exists = Friendship.objects.filter(user_from=user_from, user_to=user_to).exists()
    if not exists:
        Friendship.objects.create(user_from=user_from, user_to=user_to)


def remove_from_friends(user_from: User, user_to: User) -> bool:
    """
    Удалить пользователя из друзей/отменить заявку в друзья.
    Если пользователь сначала отправляет заявку,
    а затем удаляет из друзей, то заявка на одобрение дружбы тоже удаляется.
    Возвращает false, если ничего не произошло.
    """
    outgoing_req = Friendship.objects.filter(user_from=user_from, user_to=user_to)
    if not outgoing_req.exists():
        return False

    counter_request = Friendship.objects.filter(user_from=user_to, user_to=user_from)
    if counter_request.exists():
        if counter_request.get().request_date > outgoing_req.get().request_date:
            counter_request.delete()
    outgoing_req.delete()
    return True


def get_requests_and_friends(user_from) -> Tuple[List[User], List[User], List[User]]:
    """
    Получить входящие/исходящие заявки и друзей пользователя user_from.
    """
    possible_outgoing_req = Friendship.objects.filter(user_from=user_from)
    possible_incoming_req = Friendship.objects.filter(user_to=user_from)

    outgoing_req = []
    incoming_req = []
    friends = []

    for req in possible_outgoing_req:
        if Friendship.objects.filter(user_from=req.user_to, user_to=user_from).exists():
            friends.append(req.user_to)
        else:
            outgoing_req.append(req.user_to)

    for req in possible_incoming_req:
        if not Friendship.objects.filter(user_from=user_from, user_to=req.user_from).exists():
            incoming_req.append(req.user_from)

    return incoming_req, outgoing_req, friends


def get_friends(user_from) -> List[User]:
    """
    Получить друзей юзера
    """
    _, _, friends = get_requests_and_friends(user_from)
    return friends


def get_incoming_requests(user_from) -> List[User]:
    """
    Получить входящие заявки
    """
    incoming, _, _ = get_requests_and_friends(user_from)
    return incoming


def get_outgoing_requests(user_from) -> List[User]:
    """
    Получить исходящие заявки
    """
    _, outgoing, _ = get_requests_and_friends(user_from)
    return outgoing
