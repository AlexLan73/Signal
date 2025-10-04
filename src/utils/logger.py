"""
Настройка логирования
"""

import sys
from pathlib import Path
from loguru import logger
from src.config import settings


def setup_logger(name: str = None):
    """Настройка логгера"""
    
    # Удаляем стандартный обработчик
    logger.remove()
    
    # Консольный вывод
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Вывод в файл
    logger.add(
        settings.LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    return logger.bind(name=name or "app")
