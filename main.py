#!/usr/bin/env python3
"""
Главный файл приложения
"""

import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config import settings
from src.utils.logger import setup_logger

# Создаем необходимые директории
settings.create_directories()

logger = setup_logger(__name__)


def main():
    """Основная функция приложения"""
    logger.info("Запуск приложения")
    
    try:
        # Здесь будет основная логика приложения
        logger.info(f"Проект: {settings.PROJECT_NAME}")
        logger.info(f"Версия: {settings.PROJECT_VERSION}")
        logger.info("Приложение успешно запущено!")
        
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
