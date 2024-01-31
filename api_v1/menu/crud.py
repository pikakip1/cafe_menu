import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.menu.schemas import Menu, MenuCreate, MenuPartUpdate, MenuUpdate
from api_v1.base_crud import MenuBaseCRUD
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
    return await MenuBaseCRUD.create(session=session, upload_data=menu_data.model_dump())


async def update_menu(
        session: AsyncSession,
        menu: Menu,
        update_values: MenuPartUpdate,
) -> Menu:
    return await MenuBaseCRUD.update(
        session=session,
        update_values=update_values.model_dump(exclude_unset=True),
        obj_update=menu
    )


async def delete_menu(
    session: AsyncSession,
    menu: Menu,
) -> None:
    await MenuBaseCRUD.delete(session=session, obj_delete=menu)
