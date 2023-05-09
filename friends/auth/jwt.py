import jwt
from uuid import UUID
from datetime import datetime, timedelta
from typing import Tuple

from django.shortcuts import get_object_or_404
from ninja.security import HttpBearer

from users.models import User
from .schemas import TokenPayload
from friends import settings


ALGORITHM = settings.JWT_ALGORITHM
access_token_jwt_subject = "access"


def create_access_token(data: dict, expires_delta: timedelta = None) -> Tuple[bytes, datetime]:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def create_token(user_id: UUID) -> dict:
    access_token_expires = timedelta(minutes=settings.JWT_LIVE_TIME_MINUTES)
    access_token, expires = create_access_token(
        data={"user_id": str(user_id)}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "expires": datetime.isoformat(expires),
        "token_type": "bearer",
    }


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.PyJWTError:
        return None
    user = get_object_or_404(User, id=token_data.user_id)
    return user


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> User:
        user = get_current_user(token)
        return user
