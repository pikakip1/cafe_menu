
from fastapi import Depends, Form, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import auth.utils
from api_v1.user.schemas import ReedUser
from src.database import async_db_manager
from src.user.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login/")


async def validate_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    unauth_user_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid login or password'
    )
    stmt = select(User).filter(
        User.user_name == username
    )
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()

    if not user:
        raise unauth_user_exc

    if not auth.utils.validate_password(password, user.password):
        raise unauth_user_exc

    return user


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
):
    try:
        payload = auth.utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token',
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token not found',
        )

    res = await session.execute(select(User).filter(User.id == user_id))
    user = res.scalar_one_or_none()
    return user


def get_current_auth_and_active_user(
    user: ReedUser = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive'
    )