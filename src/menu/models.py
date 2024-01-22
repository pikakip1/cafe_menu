from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class MenuORM(Base):
    __tablename__ = "menu"

    title: Mapped[str]
    description: Mapped[str]
    sub_menus: Mapped[list["SubMenuORM"]] = relationship()


class SubMenuORM(Base):
    __tablename__ = "sub_menu"

    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))
    menu: Mapped["MenuORM"] = relationship()
    dishes: Mapped[list["DishORM"]] = relationship()


class DishORM(Base):
    __tablename__ = "dish"

    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Float(decimal_return_scale=2))
    sub_menu_id: Mapped[int] = mapped_column(
        ForeignKey("sub_menu.id", ondelete="CASCADE")
    )
