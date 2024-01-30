import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.dish import crud
from api_v1.dish.schemas import Dish, DishCreate, DishPartUpdate
from src.database import async_db_manager
from src.dish.models import DishORM

router = APIRouter(tags=['Dish'])


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/', response_model=List[Dish], status_code=status.HTTP_200_OK)
async def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> list[DishORM]:
    return await crud.get_dishes(session=session, menu_id=menu_id, submenu_id=submenu_id)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=Dish, status_code=status.HTTP_200_OK)
async def get_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> DishORM:
    return await crud.get_dish(session=session, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes/', response_model=Dish, status_code=status.HTTP_201_CREATED)
async def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        new_dish_data: DishCreate,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> DishORM:
    return await crud.create_dish(session=session, menu_id=menu_id, submenu_id=submenu_id, new_dish_data=new_dish_data)


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    status_code=status.HTTP_200_OK
)
async def update_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        update_data: DishPartUpdate,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> DishORM:
    return await crud.update_dish(
        session=session,
        menu_id=menu_id,
        sub_menu_id=submenu_id,
        dish_id=dish_id,
        update_data=update_data
    )


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK)
async def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> dict:
    return await crud.delete_dish(
        session=session,
        menu_id=menu_id,
        sub_menu_id=submenu_id,
        dish_id=dish_id
    )
