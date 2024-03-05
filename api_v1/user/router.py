
from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import auth.utils
from api_v1.user.schemas import ReedUser, CreateUser, TokenInfo, UserIn
from api_v1.user.utils import validate_user, get_current_auth_and_active_user
from src.database import async_db_manager
from src.user.models import User

router = APIRouter(tags=['User'])


@router.post('/login/', response_model=TokenInfo)
async def auth_user(
        user: UserIn = Depends(validate_user)
):
    jwt_payload = {
        'sub': str(user.id),
        'user_name': user.user_name,
        'email': user.email,
    }
    token = auth.utils.encode_jwt(payload=jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )


@router.post('/user/create/', response_model=ReedUser)
async def create_user(
        user: CreateUser,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    res = await session.execute(select(User).filter(User.user_name == user.user_name))
    if res.scalar_one_or_none():
        return {'detail': 'user with this username already exists'}
    hashed_password = await auth.utils.hash_password(user.password.decode())
    user.password = hashed_password
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get('/users/me/')
def check_auth_user_info(
        user: ReedUser = Depends(get_current_auth_and_active_user)
):
    return {
        'username': user.user_name,
        'email': user.email,
    }
