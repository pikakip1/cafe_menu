from datetime import datetime, timedelta

import jwt
import bcrypt
from src.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    custom_exp_minutes_timedelta: timedelta | None = None,
    exp_minutes: int = settings.auth_jwt.expire_token_minutes,

):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if custom_exp_minutes_timedelta:
        expire = now + custom_exp_minutes_timedelta
    else:
        expire = now + timedelta(minutes=exp_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    pub_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, pub_key, algorithms=[algorithm])
    return decoded


async def hash_password(
        password: str
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
        password: str,
        hashed_password: bytes
):
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
