# src/core/db.py
from typing import AsyncGenerator
from datetime import datetime

from sqlalchemy import Integer, DateTime
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql import func

from src.core.config import settings
from src.core.logger import logger


class PreBase:
    """Базовый класс с автоматическим именованием таблиц и полем id."""

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )


Base = declarative_base(cls=PreBase)


class BaseModel(Base):
    """Базовая абстрактная модель с полем created_at."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


engine = create_async_engine(settings.get_database_uri(), echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии базы данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def init_db() -> None:
    """Инициализация базы данных."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info(f'{init_db.__doc__} Завершено успешно')
    except Exception as error:
        logger.warning(
            f'{init_db.__doc__} Ошибка: {error}',
        )
