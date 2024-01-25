import uuid

from pydantic import BaseModel, ConfigDict


class SubMenuORMBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuORMBase):
    pass


class SubMenuUpdate(SubMenuCreate):
    pass


class SubMenuPartUpdate(SubMenuCreate):
    title: str | None = None
    description: str | None = None
    menu_id: uuid.UUID | None = None


class SubMenu(SubMenuORMBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID | str
