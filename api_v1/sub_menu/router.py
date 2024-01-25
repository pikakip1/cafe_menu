import uuid
from typing import Type, List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sub_menu.dependencies import get_sub_menu
from src.database import async_db_manager
from api_v1.sub_menu import crud
from api_v1.sub_menu.schemas import SubMenu, SubMenuCreate, SubMenuUpdate, SubMenuPartUpdate
from src.sub_menu.models import SubMenuORM

router = APIRouter(tags=["Sub menu"])


@router.get('/{menu_id}/submenus', response_model=list[SubMenu] , status_code=status.HTTP_200_OK)
async def get_sub_menus_by_menu_id(
        menu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> list[SubMenuORM] | None:

    """Функция вывода подменю по id меню"""
    return await crud.get_sub_menus(menu_id=menu_id, session=session)


@router.post('/{related_menu_id}/submenus', response_model=SubMenu, status_code=status.HTTP_201_CREATED)
async def set_sub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_data: SubMenuCreate,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> SubMenuORM:

    """Функция для создания подменю"""

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




# @router.get('/{related_menu_id}/submenus/{sub_menu_id}')
# async def get_sub_menu_by_menu_id(
#         sub_menu_id: uuid.UUID,
#         related_menu_id: uuid.UUID,
#         session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
# ) :
#     menus = await crud.get_sub_menus(session=session, menu_id=related_menu_id)
#     if sub_menu_id in menus:
#         return await crud.get_sub_menu(session=session, sub_menu_id=sub_menu_id)
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f'sub menu not found'
#     )


# @router.get('/{menu_id}/submenus')
# async def get_sub_menus(
#         menu_id: str,
#         session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
#     return await crud.get_related_submenus(menu_id=menu_id, session=session)

# @router.get('/{menu_id}/submenus{sub_menu_id}/')
# async def get_sub_menu(
#         menu_id: str,
#         sub_menu_id: str,
#         session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
#     return await crud.get_related_submenu(sub_menu_id=sub_menu_id, menu_id=menu_id, session=session)
#
#
# @router.post('/{menu_id}/submenus{sub_menu_id}/', response_model=SubMenu, status_code=status.HTTP_201_CREATED)
# async def create_sub_menu(
#         menu_id: str,
#         sub_menu_data: SubMenuCreate,
#         session: AsyncSession = Depends(async_db_manager.scoped_session_dependency),
# ):
#     return await crud.create_sub_menu(
#         menu_id=menu_id,
#         session=session,
#         sub_menu_data=sub_menu_data,
#     )
#
#
# @router.put('/{menu_id}/submenus/', response_model=SubMenu)
# async def update_sub_menu(
#         sub_menu_update: SubMenuUpdate,
#         sub_menu: SubMenu = Depends(get_sub_menu),
#         session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
# ):
#     return await crud.update_sub_menu(
#         session=session,
#         sub_menu=sub_menu,
#         sub_menu_update=sub_menu_update
#     )
#
#
# @router.patch('/{sub_menu_id}/submenus/', response_model=SubMenu)
# async def put_update_sub_menu(
#         sub_menu_update: SubMenuUpdate,
#         sub_menu: SubMenu = Depends(get_sub_menu),
#         session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
# ):
#     return await crud.update_sub_menu(
#         session=session,
#         sub_menu=sub_menu,
#         sub_menu_update=sub_menu_update,
#         part_update=True
#     )
#
#
# @router.delete("/{sub_menu_id}/submenus/", status_code=status.HTTP_200_OK)
# async def delete_sub_menu(
#     sub_menu: SubMenu = Depends(get_sub_menu),
#     session: AsyncSession = Depends(async_db_manager.scoped_session_dependency),
# ) -> None:
#     await crud.delete_sub_menu(session=session, sub_menu=sub_menu)