import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.utils.parameter_provider import ParameterProvider

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
PROJECT_ROOT = Path(__file__).parent.parent.parent

def setup_logging():
    """Настройка логирования: запись в консоль и в файл app/resources/logs/app.log."""

    level = ParameterProvider.get("log.level", "INFO").upper()
    log_file = PROJECT_ROOT / ParameterProvider.get("log.file", "app/resources/logs/app.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(file_handler)
    root.addHandler(console_handler)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

def get_logger(name):
    """Возвращает логгер модуля."""
    return logging.getLogger(name)