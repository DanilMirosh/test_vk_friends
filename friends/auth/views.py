from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from ninja import Router, Form

from .jwt import create_token, AuthBearer

from .schemas import TokenSchema, Message
from users.models import User
from users.schemas import UserSchema, UserRegistrationSchema

auth = Router(tags=["auth"])


@auth.post('/register', response={200: UserSchema, 409: Message})
def register_new_user(request, data: UserRegistrationSchema = Form(...)):
    """
    Регистрация нового юзера по логину и паролю.
    Логин должен быть до 24 символов и может содержать только латинские буквы и цифры.
    """
    username = data.username
    if User.objects.filter(username=username).exists():
        return 409, {"detail": "This username is already taken"}
    return User.objects.create_user(**data.dict())


@auth.post('/login', response={200: TokenSchema, 400: Message, 404: Message})
def login(request, data: UserRegistrationSchema = Form(...)):
    """
    Получить access token
    """
    user = get_object_or_404(User, username=data.username)
    if check_password(data.password, user.password):
        return create_token(user.id)
    return 400, {"detail": "Password is not correct"}


@auth.get('/whoami', auth=AuthBearer(), response={200: UserSchema, 401: Message})
def get_my_nickname(request):
    """
    Получить пользователя по токену
    """
    return request.auth
