import uuid
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from api_v1.dependencies import check_menu_id, get_menu
from api_v1.sub_menu.schemas import SubMenuCreate, SubMenuPartUpdate
from src.sub_menu.models import SubMenuORM


async def get_sub_menus(
        menu_id: uuid.UUID,
        session: AsyncSession
) -> Sequence[SubMenuORM]:
    await check_menu_id(session=session, menu_id=menu_id)
    stmt = select(SubMenuORM).filter(SubMenuORM.menu_id == menu_id).options(selectinload(SubMenuORM.dishes))

    result = await session.execute(stmt)
    sub_menus = result.scalars().all()
    for sub_menu in sub_menus:
        sub_menu.dishes_count = len(sub_menu.dishes)
    return sub_menus


async def create_sub_menu(
        session: AsyncSession,
        related_menu_id: uuid.UUID,
        sub_menu_data: SubMenuCreate
) -> SubMenuORM:
    menu = await get_menu(session=session, menu_id=related_menu_id)

    sub_menu = SubMenuORM(**sub_menu_data.model_dump())
    sub_menu.menu_id = menu.id
    session.add(sub_menu)
    await session.commit()
    return sub_menu


async def get_sub_menu_by_menu_id(
        session: AsyncSession,
        sub_menu_id: uuid.UUID,
        related_menu_id: uuid.UUID
) -> SubMenuORM:
    await check_menu_id(session=session, menu_id=related_menu_id)
    stmt = select(SubMenuORM).filter(
        (SubMenuORM.menu_id == related_menu_id) &
        (SubMenuORM.id == sub_menu_id)
    ).options(selectinload(SubMenuORM.dishes))

    result = await session.execute(stmt)
    sub_menu = result.scalars().first()

    if not sub_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
    sub_menu.dishes_count = len(sub_menu.dishes)
    return sub_menu


async def update_sub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        update_data: SubMenuPartUpdate,
        session: AsyncSession
) -> SubMenuORM:
    sub_menu = await get_sub_menu_by_menu_id(
        session=session,
        sub_menu_id=sub_menu_id,
        related_menu_id=related_menu_id
    )
    for name, value in update_data.model_dump(exclude_unset=True).items():
        setattr(sub_menu, name, value)
    await session.commit()
    await session.refresh(sub_menu)
    return sub_menu


async def delete_cub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        session: AsyncSession
) -> None:
    sub_menu = await get_sub_menu_by_menu_id(session=session, sub_menu_id=sub_menu_id, related_menu_id=related_menu_id)
    await session.delete(sub_menu)
    await session.commit()
