import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from api_v1.dependencies import get_sub_menu_by_menu_id
from api_v1.base_crud import DishBaseCRUD
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
    data = new_dish_data.model_dump()
    data.update(sub_menu_id=sub_menu.id)
    return await DishBaseCRUD.create(
        session=session,
        upload_data=data
    )


async def update_dish(
        menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        dish_id: uuid.UUID,
        update_data: DishPartUpdate,
        session: AsyncSession
) -> DishORM:
    dish = await get_dish(session=session, menu_id=menu_id, submenu_id=sub_menu_id, dish_id=dish_id)
    return await DishBaseCRUD.update(
        session=session,
        update_values=update_data.model_dump(exclude_unset=True),
        obj_update=dish
    )


async def delete_dish(
        menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: AsyncSession
) -> None:
    dish = await get_dish(session=session, menu_id=menu_id, submenu_id=sub_menu_id, dish_id=dish_id)
    await DishBaseCRUD.delete(
        session=session,
        obj_delete=dish
    )
