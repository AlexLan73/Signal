"""
Тесты основного модуля
"""

import pytest
from src.config import settings


def test_settings():
    """Тест настроек"""
    assert settings.PROJECT_NAME is not None
    assert settings.PROJECT_VERSION is not None


def test_logs_dir_exists():
    """Тест создания директории логов"""
    assert settings.LOGS_DIR.exists()


if __name__ == "__main__":
    pytest.main([__file__])
