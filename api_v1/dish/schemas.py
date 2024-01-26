import uuid

from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass


class DishUpdate(DishCreate):
    pass


class DishPartUpdate(DishUpdate):
    title: str | None = None
    description: str | None = None
    menu_id: uuid.UUID | None = None
    price: float | None = None


class Dish(DishBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID | str
