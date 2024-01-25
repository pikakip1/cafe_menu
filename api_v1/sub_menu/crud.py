import uuid

from fastapi import HTTPException
from sqlalchemy import select, and_, exists
from sqlalchemy.exc import NoResultFound
from starlette import status

from api_v1.dependencies import get_menu
from src.menu.models import MenuORM
from src.sub_menu.models import SubMenuORM
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.sub_menu.schemas import SubMenuCreate, SubMenuPartUpdate


async def get_sub_menus(
        menu_id: uuid.UUID,
        session: AsyncSession
):
    menu = await get_menu(session=session, menu_id=menu_id)
    sub_menus = await session.scalars(select(SubMenuORM).filter(SubMenuORM.menu_id == menu.id))
    return sub_menus


async def create_sub_menu(
        session: AsyncSession,
        related_menu_id: uuid.UUID,
        sub_menu_data: SubMenuCreate
) -> SubMenuORM:
    stmt = await session.execute(select(MenuORM).filter(MenuORM.id == related_menu_id))
    if not stmt.scalars().all():
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f'Menu has no id {related_menu_id}'
        )
    sub_menu = SubMenuORM(**sub_menu_data.model_dump())
    sub_menu.menu_id = related_menu_id
    session.add(sub_menu)
    await session.commit()
    await session.refresh(sub_menu)

    return sub_menu


async def get_sub_menu_by_menu_id(
        session: AsyncSession,
        sub_menu_id: uuid.UUID,
        related_menu_id: uuid.UUID
) -> list | SubMenuORM:
    menu = await get_menu(session=session, menu_id=related_menu_id)
    response = await session.scalars(
        select(SubMenuORM).
        filter(
            and_(SubMenuORM.menu_id == menu.id, SubMenuORM.id == sub_menu_id)
        ))
    sub_menu = response.first()
    if not sub_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'submenu not found'
        )
    return sub_menu


async def update_sub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        update_data: SubMenuPartUpdate,
        session: AsyncSession
) -> SubMenuORM:
    sub_menu = await get_sub_menu_by_menu_id(session=session, sub_menu_id=sub_menu_id, related_menu_id=related_menu_id)
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

#----------------------------------------- helper func


async def check_menu_id(
        menu_id: uuid.UUID,
        session: AsyncSession
) -> None:
    query = select(exists().where(MenuORM.id == menu_id))
    exists_menu = await session.scalar(query)
    if not exists_menu:
        raise NoResultFound('menu not found')


async def get_sub_menu(
        sub_menu_id: uuid.UUID,
        session: AsyncSession
) -> SubMenuORM:
    return await session.get(SubMenuORM.id, sub_menu_id)
