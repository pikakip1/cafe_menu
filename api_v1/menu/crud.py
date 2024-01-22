import uuid

from sqlalchemy.engine import Result
from sqlalchemy import select

from src.menu.models import MenuORM

from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.menu.schemas import Menu, MenuCreate


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
