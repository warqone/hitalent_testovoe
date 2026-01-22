from enum import Enum

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class DBEngine(str, Enum):
    """Поддерживаемые движки баз данных для приложения."""

    SQLITE = 'sqlite'
    POSTGRES = 'postgres'


class Settings(BaseSettings):
    """Настройки проекта."""

    # -------------------
    # Общие настройки
    # -------------------
    app_title: str = 'Чаты и сообщения'
    description: str = 'API чатов и сообщений'
    debug: bool = True

    # -------------------
    # Настройки БД
    # -------------------
    db_engine: DBEngine = Field(default=DBEngine.POSTGRES, env='DB_ENGINE')
    db_host: str = Field(..., env='DB_HOST')
    db_port: int = Field(..., env='DB_PORT')
    db_name: str = Field(..., env='DB_NAME')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    # -------------------
    # Настройки повторных попыток БД
    # -------------------
    db_retry_max_attempts: int = Field(..., env='DB_RETRY_MAX_ATTEMPTS')
    db_retry_delay_seconds: float = Field(..., env='DB_RETRY_DELAY_SECONDS')

    # -------------------
    # Методы
    # -------------------
    def get_database_uri(self) -> str:
        """Возвращает URI для подключения к базе данных."""
        if self.db_engine == DBEngine.POSTGRES:
            return (
                f'postgresql+asyncpg://{self.db_user}:{self.db_password}'
                f'@{self.db_host}:{self.db_port}/{self.db_name}'
            )
        return f'sqlite+aiosqlite:///./{self.db_name}'

    model_config = ConfigDict(
        env_file='.env',
        extra='allow',
        case_sensitive=False,
    )


settings = Settings()
