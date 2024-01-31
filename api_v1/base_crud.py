from sqlalchemy.ext.asyncio import AsyncSession

from src.dish.models import DishORM
from src.menu.models import MenuORM
from src.sub_menu.models import SubMenuORM


class BaseCRUD:
    model = None

    @classmethod
    async def create(cls, session: AsyncSession, upload_data: dict):
        new_obj = cls.model(**upload_data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    @classmethod
    async def update(cls, session: AsyncSession, update_values: dict, obj_update: model):
        for name, value in update_values.items():
            setattr(obj_update, name, value)
        await session.commit()
        await session.refresh(obj_update)
        return obj_update

    @classmethod
    async def delete(cls, session: AsyncSession, obj_delete: model):
        await session.delete(obj_delete)
        await session.commit()


class SubMenuBaseCRUD(BaseCRUD):
    model = SubMenuORM


class MenuBaseCRUD(BaseCRUD):
    model = MenuORM


class DishBaseCRUD(BaseCRUD):
    model = DishORM
