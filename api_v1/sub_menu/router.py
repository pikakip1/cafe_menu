import uuid
from typing import Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sub_menu import crud
from api_v1.sub_menu.schemas import SubMenu, SubMenuCreate, SubMenuPartUpdate
from src.database import async_db_manager
from src.sub_menu.models import SubMenuORM

router = APIRouter(tags=["Sub menu"])


@router.get('/{menu_id}/submenus', response_model=list[SubMenu], status_code=status.HTTP_200_OK)
async def get_sub_menus_by_menu_id(
        menu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> Sequence[SubMenuORM]:
    return await crud.get_sub_menus(menu_id=menu_id, session=session)


@router.post('/{related_menu_id}/submenus', response_model=SubMenu, status_code=status.HTTP_201_CREATED)
async def set_sub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_data: SubMenuCreate,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> SubMenuORM:
    return await crud.create_sub_menu(sub_menu_data=sub_menu_data, session=session, related_menu_id=related_menu_id)


@router.get('/{related_menu_id}/submenus/{sub_menu_id}/', response_model=SubMenu, status_code=status.HTTP_200_OK)
async def get_sub_menu_by_menu_id(
        sub_menu_id: uuid.UUID,
        related_menu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> SubMenuORM:
    return await crud.get_sub_menu_by_menu_id(sub_menu_id=sub_menu_id, session=session, related_menu_id=related_menu_id)


@router.patch('/{related_menu_id}/submenus/{sub_menu_id}/', response_model=SubMenu)
async def update_sub_menu(
        related_menu_id: uuid.UUID,
        update_data: SubMenuPartUpdate,
        sub_menu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> SubMenuORM:
    return await crud.update_sub_menu(
        session=session,
        sub_menu_id=sub_menu_id,
        related_menu_id=related_menu_id,
        update_data=update_data
    )


@router.delete('/{related_menu_id}/submenus/{sub_menu_id}/')
async def delete_sub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> None:
    await crud.delete_cub_menu(
        related_menu_id=related_menu_id,
        sub_menu_id=sub_menu_id,
        session=session
    )
