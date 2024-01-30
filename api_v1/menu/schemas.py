import uuid

from pydantic import BaseModel, ConfigDict


class MenuORMBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuORMBase):
    pass


class MenuUpdate(MenuCreate):
    pass


class MenuPartUpdate(MenuCreate):
    title: str | None = None
    description: str | None = None


class Menu(MenuORMBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID | str
    submenus_count: int = 0
    dishes_count: int = 0
