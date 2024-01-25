import uuid

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated, Any

from api_v1.sub_menu import crud
from src.database import async_db_manager
from src.sub_menu.models import SubMenuORM


async def get_sub_menu(
        sub_menu_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> SubMenuORM:
    sub_menu = await crud.get_sub_menu(session=session,sub_menu_id=sub_menu_id)
    if sub_menu:
        return sub_menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'submenu not found'
    )



