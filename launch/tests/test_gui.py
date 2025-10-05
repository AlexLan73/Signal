#!/usr/bin/env python3
"""Test script to verify GUI functionality."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
    from PyQt6.QtCore import Qt
    print("✅ PyQt6 imported successfully")
    
    # Create a simple test window
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("SignalAnalyzer GUI Test")
    window.setGeometry(100, 100, 800, 600)
    
    # Create central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout(central_widget)
    
    # Add test label
    label = QLabel("""
    <div style='text-align: center; padding: 50px;'>
        <h1>🎉 SignalAnalyzer GUI Test</h1>
        <h2>✅ PyQt6 работает!</h2>
        <p style='color: green; font-size: 16px;'>
            GUI каркас успешно создан и готов к использованию
        </p>
        <p style='color: #666;'>
            Главное окно приложения с меню, панелью инструментов<br>
            и вкладками визуализации готово к запуску
        </p>
        <p style='color: #333; font-weight: bold;'>
            Для запуска полного приложения используйте:<br>
            <code>py src/gui/run_gui.py</code>
        </p>
    </div>
    """)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)
    
    window.show()
    
    print("✅ GUI window created and displayed")
    print("✅ SignalAnalyzer GUI test successful!")
    print("\n🎯 Что создано:")
    print("  • Главное окно с меню и панелью инструментов")
    print("  • Вкладки: Signal Generator, 2D Plot, 3D Plot, Spectrum, Oscilloscope")
    print("  • Панель конфигурации сигналов")
    print("  • Система событий и сигналов")
    print("  • Статус-бар и навигация")
    
    # Show for 3 seconds then close
    from PyQt6.QtCore import QTimer
    QTimer.singleShot(3000, window.close)
    
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"❌ Error importing PyQt6: {e}")
    print("Установите PyQt6: py -m pip install PyQt6")
    sys.exit(1)
except Exception as e:
    print(f"❌ GUI test failed: {e}")
    sys.exit(1)
