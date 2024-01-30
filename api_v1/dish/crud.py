import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from api_v1.dependencies import get_sub_menu_by_menu_id
from api_v1.dish.schemas import DishCreate, DishPartUpdate
from src.dish.models import DishORM
from src.sub_menu.models import SubMenuORM


async def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession
) -> list[DishORM] | None:
    try:
        sub_menu = await get_sub_menu_by_menu_id(session=session, related_menu_id=menu_id, sub_menu_id=submenu_id)
    except HTTPException:
        return []
    result = await session.execute(
            select(SubMenuORM).
            options(selectinload(SubMenuORM.dishes))
            .where(SubMenuORM.id == sub_menu.id)
        )
    sub_menu_with_dishes = result.scalars().first()
    return sub_menu_with_dishes.dishes


async def get_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: AsyncSession
) -> DishORM | None:
    sub_menu = await get_sub_menu_by_menu_id(session=session, related_menu_id=menu_id, sub_menu_id=submenu_id)
    stmt = (select(DishORM).
            filter(
        (DishORM.sub_menu_id == sub_menu.id) &
        (DishORM.id == dish_id)
    ))
    result = await session.execute(stmt)
    dish = result.scalars().first()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )
    return dish


async def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        new_dish_data: DishCreate,
        session: AsyncSession
) -> DishORM:
    sub_menu = await get_sub_menu_by_menu_id(session=session, related_menu_id=menu_id,  sub_menu_id=submenu_id)
    new_dish = DishORM(**new_dish_data.model_dump())
    new_dish.sub_menu_id = sub_menu.id
    session.add(new_dish)
    await session.commit()
    return new_dish


async def update_dish(
        menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        dish_id: uuid.UUID,
        update_data: DishPartUpdate,
        session: AsyncSession
) -> DishORM:
    dish = await get_dish(session=session, menu_id=menu_id, submenu_id=sub_menu_id, dish_id=dish_id)
    for name, value in update_data.model_dump(exclude_unset=True).items():
        setattr(dish, name, value)
    await session.commit()
    await session.refresh(dish)
    return dish


async def delete_dish(
        menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: AsyncSession
) -> dict:
    dish = await get_dish(session=session, menu_id=menu_id, submenu_id=sub_menu_id, dish_id=dish_id)
    dish_title = dish.title
    await session.delete(dish)
    await session.commit()
    return {'Блюдо удалено': dish_title}
