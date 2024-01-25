import uuid

from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
import src.sub_menu.models


class DishORM(Base):
    __tablename__ = "dish"

    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Float(decimal_return_scale=2))
    sub_menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sub_menu.id", ondelete="CASCADE")
    )
    sub_menu: Mapped["SubMenuORM"] = relationship(
        back_populates='dishes'
    )