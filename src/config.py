"""
Конфигурация приложения
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Путь к корневой директории проекта
BASE_DIR = Path(__file__).parent.parent

class Settings:
    """Настройки приложения"""
    
    # Основные настройки
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Python Project")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # API
    API_KEY: str = os.getenv("API_KEY", "")
    
    # Логирование
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Сервер
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Пути
    LOGS_DIR: Path = BASE_DIR / "logs"
    DATA_DIR: Path = BASE_DIR / "data"
    
    def create_directories(self):
        """Создаем необходимые директории"""
        self.LOGS_DIR.mkdir(exist_ok=True)
        self.DATA_DIR.mkdir(exist_ok=True)

# Глобальный экземпляр настроек
settings = Settings()
