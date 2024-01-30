import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.dish.models
import src.menu.models
from src.database import Base


class SubMenuORM(Base):
    __tablename__ = "sub_menu"

    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))

    menu: Mapped["MenuORM"] = relationship(
        back_populates='sub_menus'
    )

    dishes: Mapped[list["DishORM"]] = relationship(
        back_populates='sub_menu',
        cascade='all, delete-orphan'
    )
