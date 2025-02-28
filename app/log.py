"""Конфигурация логирования"""

from loguru import logger

logger.add(
    "loguru/best_parking_db.log",
    level="INFO",
    format="{time}**{level}**{message}",
    rotation="10 MB",
)
