import uuid
from typing import Type

from sqlalchemy.engine import Result
from sqlalchemy import select

from api_v1.sub_menu.schemas import SubMenu
from src.menu.models import MenuORM
from src.sub_menu.models import SubMenuORM

from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.menu.schemas import Menu, MenuCreate, MenuUpdate, MenuPartUpdate


async def get_all_menus(session: AsyncSession) -> list[MenuORM]:
    stmt = select(MenuORM)
    result: Result = await session.execute(stmt)
    menus = result.scalars().all()
    return list(menus)


async def get_menu(session: AsyncSession, menu_id: uuid.UUID) -> MenuORM | None:
    return await session.get(MenuORM, menu_id)


async def create_menu(session: AsyncSession, menu_data: MenuCreate) -> MenuORM:
    menu = MenuORM(**menu_data.model_dump())
    session.add(menu)
    await session.commit()
    return menu


async def update_menu(
        session: AsyncSession,
        menu: Menu,
        menu_update: MenuUpdate | MenuPartUpdate,
        part_update: bool = False
) -> Menu:
    for name, value in menu_update.model_dump(exclude_unset=part_update).items():
        setattr(menu, name, value)
    await session.commit()
    await session.refresh(menu)
    return menu


async def delete_menu(
    session: AsyncSession,
    menu: Menu,
) -> None:
    await session.delete(menu)
    await session.commit()


