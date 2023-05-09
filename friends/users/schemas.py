from uuid import UUID

from ninja import Schema
from pydantic import validator


class UserSchema(Schema):
    username: str = "SomeUsername"
    id: UUID


class UserRegistrationSchema(Schema):
    username: str
    password: str

    @validator('username')
    def name_length_and_length(cls, v):
        assert v.isalnum(), 'username must be alphanumeric'
        assert len(v) <= 24, 'username must be shorter than 24 symbols'
        return v
