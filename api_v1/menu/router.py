from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menu import crud
from api_v1.dependencies import get_menu
from api_v1.menu.schemas import Menu, MenuCreate, MenuPartUpdate, MenuUpdate
from src.database import async_db_manager

router = APIRouter(tags=["Menu"])


@router.get('/', response_model=list[Menu])
async def get_menus(session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    return await crud.get_all_menus(session=session)


@router.get('/{menu_id}', response_model=Menu)
async def get_menu(menu: Menu = Depends(get_menu)):
    return menu


@router.post('/', response_model=Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(
        menu_data: MenuCreate,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    return await crud.create_menu(session=session, menu_data=menu_data)


@router.put('/', response_model=Menu)
async def update_menu(
        menu_update: MenuPartUpdate,
        menu: Menu = Depends(get_menu),
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
):
    return await crud.update_menu(
        session=session,
        menu=menu,
        update_values=menu_update
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
        update_values=menu_update,
    )


@router.delete("/{menu_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    menu: Menu = Depends(get_menu),
    session: AsyncSession = Depends(async_db_manager.scoped_session_dependency),
) -> None:
    await crud.delete_menu(session=session, menu=menu)
