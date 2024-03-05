from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_name: str
    password: bytes
    active: bool


class ReedUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_name: str
    active: bool


class UserIn(BaseModel):
    user_name: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
