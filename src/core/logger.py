import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.constants import (
    BACKUP_COUNT_TEMP_LOGER,
    LOG_FILE_APP_LOGGER,
    MAX_BYTES_TEMP_LOGER,
)


class FastAPILogger(Logger):
    """Логгер для FastAPI."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """Инициализация логгера."""
        super().__init__(name, level)
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Настройка обработчиков логов."""
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S',
        )

        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        file_handler = RotatingFileHandler(
            log_dir / LOG_FILE_APP_LOGGER,
            maxBytes=MAX_BYTES_TEMP_LOGER,
            backupCount=BACKUP_COUNT_TEMP_LOGER,
            encoding='utf-8',
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.addHandler(file_handler)
        self.addHandler(console_handler)

        self.propagate = False


logger: FastAPILogger = FastAPILogger(__name__)
