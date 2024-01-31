import uuid
from typing import Sequence, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1 import dependencies
from api_v1.base_crud import SubMenuBaseCRUD
from api_v1.sub_menu.schemas import SubMenuCreate, SubMenuPartUpdate
from src.sub_menu.models import SubMenuORM



async def get_sub_menus(
        menu_id: uuid.UUID,
        session: AsyncSession
) -> Sequence[SubMenuORM]:
    await dependencies.check_menu_id(session=session, menu_id=menu_id)
    stmt = select(SubMenuORM).filter(SubMenuORM.menu_id == menu_id).options(selectinload(SubMenuORM.dishes))

    result = await session.execute(stmt)
    sub_menus = result.scalars().all()
    for sub_menu in sub_menus:
        sub_menu.dishes_count = len(sub_menu.dishes)
    return sub_menus


async def create_sub_menu(
        session: AsyncSession,
        related_menu_id: uuid.UUID,
        sub_menu_data: SubMenuCreate
) -> SubMenuORM:
    await dependencies.check_menu_id(session=session, menu_id=related_menu_id)
    data = sub_menu_data.model_dump()
    data.update(menu_id=related_menu_id)
    return await SubMenuBaseCRUD.create(session=session, upload_data=data)


async def get_sub_menu_by_menu_id(
        session: AsyncSession,
        sub_menu_id: uuid.UUID,
        related_menu_id: uuid.UUID
) -> SubMenuORM | list[Any]:
    return await dependencies.get_sub_menu_by_menu_id(
        session=session,
        related_menu_id=related_menu_id,
        sub_menu_id=sub_menu_id
    )


async def update_sub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        update_data: SubMenuPartUpdate,
        session: AsyncSession
) -> SubMenuORM:
    sub_menu = await get_sub_menu_by_menu_id(
        session=session,
        sub_menu_id=sub_menu_id,
        related_menu_id=related_menu_id
    )
    return await SubMenuBaseCRUD.update(
        session=session,
        update_values=update_data.model_dump(exclude_unset=True),
        obj_update=sub_menu
    )


async def delete_cub_menu(
        related_menu_id: uuid.UUID,
        sub_menu_id: uuid.UUID,
        session: AsyncSession
) -> None:
    sub_menu = await dependencies.get_sub_menu_by_menu_id(
        session=session,
        sub_menu_id=sub_menu_id,
        related_menu_id=related_menu_id
    )
    await SubMenuBaseCRUD.delete(
        session=session,
        obj_delete=sub_menu
    )
