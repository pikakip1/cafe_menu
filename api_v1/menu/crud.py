import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.menu.schemas import Menu, MenuCreate, MenuPartUpdate, MenuUpdate
from src.menu.models import MenuORM
from src.sub_menu.models import SubMenuORM


async def get_all_menus(session: AsyncSession) -> list[MenuORM]:
    stmt = select(MenuORM).options(selectinload(MenuORM.sub_menus).options(selectinload(SubMenuORM.dishes)))

    result = await session.execute(stmt)
    menus = result.scalars().all()
    for menu in menus:
        menu.submenus_count = len(menu.sub_menus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.sub_menus)
    return menus


async def get_menu(session: AsyncSession, menu_id: uuid.UUID) -> list[Any] | MenuORM:
    stmt = (
        select(MenuORM).
        filter(MenuORM.id == menu_id)
        .options(
            selectinload(MenuORM.sub_menus).options(selectinload(SubMenuORM.dishes))
        )
    )
    result = await session.execute(stmt)
    menu = result.scalars().one_or_none()
    if not menu:
        return []
    menu.submenus_count = len(menu.sub_menus)
    menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.sub_menus)
    return menu


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
