import uuid

from pydantic import BaseModel, ConfigDict


class MenuORMBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuORMBase):
    pass


class Menu(MenuORMBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID | str
