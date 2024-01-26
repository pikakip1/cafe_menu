import uuid
from typing import Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select, and_, exists, Row, RowMapping, Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload
from starlette import status
from api_v1.sub_menu.crud import get_sub_menu_by_menu_id
from api_v1.dependencies import get_menu, get_sub_menu
from src.dish.models import DishORM
from src.menu.models import MenuORM
from src.sub_menu.models import SubMenuORM
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.sub_menu.schemas import SubMenuCreate, SubMenuPartUpdate


async def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession
) -> list[DishORM] | None:

    sub_menu = await get_sub_menu_by_menu_id(session=session, related_menu_id=menu_id, sub_menu_id=submenu_id)
    result = await session.execute(
        select(SubMenuORM).
        options(selectinload(SubMenuORM.dishes))
        .where(SubMenuORM.id == sub_menu.id)
    )
    sub_menu_load = result.scalars().first()
    return sub_menu_load.dishes
