import uuid
from typing import Type, List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.dish.schemas import Dish
from api_v1.sub_menu.dependencies import get_sub_menu
from src.database import async_db_manager
from api_v1.dish import crud
from api_v1.sub_menu.schemas import SubMenu, SubMenuCreate, SubMenuUpdate, SubMenuPartUpdate
from src.dish.models import DishORM
from src.sub_menu.models import SubMenuORM


router = APIRouter(tags=['Dish'])


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/', response_model=List[Dish], status_code=status.HTTP_200_OK)
async def get_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> list[DishORM]:
    return await crud.get_dishes(session=session, menu_id=menu_id, submenu_id=submenu_id)
