#!/usr/bin/env python3
"""Главный файл запуска SignalAnalyzer GUI в PyCharm."""

import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Импортируем и запускаем главное окно
from src.gui.main_window import main

if __name__ == "__main__":
    print("🚀 Запуск SignalAnalyzer GUI...")
    print("📁 Рабочая директория:", project_root)
    print("🐍 Python:", sys.executable)
    print("📦 Модули:", sys.path[:3])
    print("-" * 50)
    
    main()
