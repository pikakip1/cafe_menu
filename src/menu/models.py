from sqlalchemy.orm import Mapped, relationship

from src.database import Base
import src.sub_menu.models


class MenuORM(Base):
    __tablename__ = "menu"

    title: Mapped[str]
    description: Mapped[str]
    sub_menus: Mapped[list["SubMenuORM"]] = relationship(
        back_populates='menu'

    )
