from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from src.config import settings
import uuid
from datetime import datetime
from asyncio import current_task
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import DeclarativeBase


class AsyncDatabaseManager:
    async_engine = create_async_engine(
        url=settings.DATABASE_URL_asyncpg,
        echo=True,
    )
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.async_session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self):
        with self.get_scoped_session() as async_session:
            yield async_session
            await async_session.remove()

    async def scoped_session_dependency(self):
        async_session = self.get_scoped_session()
        yield async_session
        await async_session.close()


async_db_manager = AsyncDatabaseManager()


class Base(DeclarativeBase):
    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for ind, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or ind < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f'<{self.__class__.__name__} {", ".join(cols)}>'
