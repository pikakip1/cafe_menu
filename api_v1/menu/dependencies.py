import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.menu import crud
from src.database import async_db_manager
from src.menu.models import MenuORM


async def get_menu(
        menu_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(async_db_manager.scoped_session_dependency)
) -> MenuORM:
    menu = await crud.get_menu(session=session, menu_id=menu_id)
    if menu:
        return menu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='menu not found'
    )
