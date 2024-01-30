import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.sub_menu.models
from src.database import Base


class DishORM(Base):
    __tablename__ = "dish"

    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(DECIMAL(decimal_return_scale=2))
    sub_menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sub_menu.id", ondelete="CASCADE")
    )
    sub_menu: Mapped["SubMenuORM"] = relationship(
        back_populates='dishes'
    )
