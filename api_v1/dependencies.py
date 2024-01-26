import uuid

from fastapi import Depends, HTTPException, Path
from sqlalchemy import select, exists
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated

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
        detail=f'menu not found'
    )


async def get_sub_menu(
        sub_menu_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> SubMenuORM:
    sub_menu = await sub_menu_crud.get_sub_menu(session=session, sub_menu_id=sub_menu_id)
    if sub_menu:
        return sub_menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'submenu not found'
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
            detail=f'menu not found'
        )


async def check_sub_menu_id(
        sub_menu_id: uuid.UUID,
        session: AsyncSession
) -> None:
    query = select(exists().where(SubMenuORM.id == sub_menu_id))
    exists_menu = await session.scalar(query)
    if not exists_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'submenu not found'
        )
