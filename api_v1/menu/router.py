import uuid

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menu.dependencies import get_menu
from src.database import async_db_manager
from api_v1.menu import crud
from api_v1.menu.schemas import Menu, MenuCreate, MenuUpdate, MenuPartUpdate

router = APIRouter(tags=["Menu"])


@router.get('/', response_model=list[Menu])
async def get_menus(session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    return await crud.get_all_menus(session=session)


@router.get('/{menu_id}', response_model=Menu)
async def get_menu(menu: Menu = Depends(get_menu)):
    return menu


@router.post('/', response_model=Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu_data: MenuCreate, session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    return await crud.create_menu(session=session, menu_data=menu_data)


@router.put('/', response_model=Menu)
async def update_menu(
        menu_update: MenuUpdate,
        menu: Menu = Depends(get_menu),
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    return await crud.update_menu(
        session=session,
        menu=menu,
        menu_update=menu_update
    )


@router.patch('/{menu_id}', response_model=Menu)
async def put_update_menu(
        menu_update: MenuPartUpdate,
        menu: Menu = Depends(get_menu),
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    return await crud.update_menu(
        session=session,
        menu=menu,
        menu_update=menu_update,
        part_update=True
    )


@router.delete("/{menu_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    menu: Menu = Depends(get_menu),
    session: AsyncSession = Depends(async_db_manager.scoped_session_dependency),
) -> None:
    await crud.delete_menu(session=session, menu=menu)