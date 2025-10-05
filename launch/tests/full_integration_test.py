#!/usr/bin/env python3
"""Запуск полного интеграционного теста в PyCharm."""

import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Импортируем и запускаем полный интеграционный тест
if __name__ == "__main__":
    print("🔗 Запуск полного интеграционного теста...")
    print("📁 Рабочая директория:", project_root)
    print("🐍 Python:", sys.executable)
    print("-" * 50)
    
    # Динамический импорт для избежания ошибок
    try:
        from test_full_integration import *
        print("✅ Полный интеграционный тест импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("  py -m pip install PyQt6 matplotlib numpy")
        sys.exit(1)
