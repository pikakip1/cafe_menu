import uuid

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_db_manager
from api_v1.menu import crud
from api_v1.menu.schemas import Menu, MenuCreate

router = APIRouter(tags=["Menu"])


@router.get('/', response_model=list[Menu])
async def get_menus(session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    return await crud.get_all_menus(session=session)


@router.get('/{menu_id}', response_model=Menu)
async def get_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    product = await crud.get_menu(session=session, menu_id=menu_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Menu with id {menu_id} not found'
    )


@router.post('/', response_model=Menu)
async def create_menu(menu_data: MenuCreate, session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)):
    return await crud.create_menu(session=session, menu_data=menu_data)
