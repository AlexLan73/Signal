#!/usr/bin/env python3
"""Запуск теста математического движка в PyCharm."""

import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Импортируем и запускаем тест математического движка
if __name__ == "__main__":
    print("🧮 Запуск теста математического движка...")
    print("📁 Рабочая директория:", project_root)
    print("🐍 Python:", sys.executable)
    print("-" * 50)
    
    # Динамический импорт для избежания ошибок
    try:
        from test_math_engine import *
        print("✅ Тест математического движка импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что все зависимости установлены:")
        print("  py -m pip install numpy matplotlib")
        sys.exit(1)
