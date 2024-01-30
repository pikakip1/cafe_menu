from sqlalchemy.orm import Mapped, relationship

import src.sub_menu.models
from src.database import Base


class MenuORM(Base):
    __tablename__ = "menu"

    title: Mapped[str]
    description: Mapped[str]
    sub_menus: Mapped[list["SubMenuORM"]] = relationship(
        back_populates='menu',
        cascade='all, delete-orphan'
    )
