import uuid
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Path
from sqlalchemy import and_, exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.menu import crud as menu_crud
from api_v1.sub_menu import crud as sub_menu_crud
from src.database import async_db_manager
from src.menu.models import MenuORM
from src.sub_menu.models import SubMenuORM


async def get_menu(
        menu_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> MenuORM:
    menu = await menu_crud.get_menu(session=session, menu_id=menu_id)
    if menu:
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='menu not found'
    )


async def check_menu_id(
        menu_id: uuid.UUID,
        session: AsyncSession
) -> None:
    query = select(exists().where(MenuORM.id == menu_id))
    exists_menu = await session.scalar(query)
    if not exists_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )


async def check_sub_menu_id(
        sub_menu_id: uuid.UUID,
        menu_id: uuid.UUID,
        session: AsyncSession
) -> None:
    query = select(exists().where(and_(SubMenuORM.id == sub_menu_id, SubMenuORM.menu_id == menu_id)))
    exists_menu = await session.scalar(query)
    if not exists_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found',
        )


async def get_sub_menu_by_menu_id(
        session: AsyncSession,
        sub_menu_id: uuid.UUID,
        related_menu_id: uuid.UUID
) -> SubMenuORM | list[Any]:
    return await sub_menu_crud.get_sub_menu_by_menu_id(
        session=session,
        related_menu_id=related_menu_id,
        sub_menu_id=sub_menu_id
    )
