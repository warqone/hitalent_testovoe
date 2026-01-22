from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.constants import TAGS_METADATA
from src.core.db import init_db
from src.core.logger import logger
from src.api.routers import main_router
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Инициализация БД."""
    logger.info('Запуск приложения, инициализация БД...')
    await init_db()
    yield
    logger.info('Приложение завершает работу')

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    lifespan=lifespan,
    openapi_tags=TAGS_METADATA,
)

app.include_router(main_router)
