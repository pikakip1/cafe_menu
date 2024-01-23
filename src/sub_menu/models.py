import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
import src.dish.models
import src.menu.models


class SubMenuORM(Base):
    __tablename__ = "sub_menu"

    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))

    menu: Mapped["MenuORM"] = relationship(
        back_populates='sub_menus'
    )

    dishes: Mapped[list["DishORM"]] = relationship(
        back_populates='sub_menu'
    )
