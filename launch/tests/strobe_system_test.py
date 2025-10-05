#!/usr/bin/env python3
"""Запуск теста системы стробов в PyCharm."""

import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Импортируем и запускаем тест системы стробов
if __name__ == "__main__":
    print("🎯 Запуск теста системы стробов...")
    print("📁 Рабочая директория:", project_root)
    print("🐍 Python:", sys.executable)
    print("-" * 50)
    
    # Динамический импорт для избежания ошибок
    try:
        from test_strobe_system import *
        print("✅ Тест системы стробов импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("  py -m pip install PyQt6 matplotlib numpy")
        sys.exit(1)
