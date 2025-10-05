#!/usr/bin/env python3
"""Test script for SignalAnalyzer strobe system."""

import sys
from pathlib import Path
import numpy as np

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
    from PyQt6.QtCore import Qt
    
    from src.gui.strobe_widget import StrobeConfigWidget
    from src.visualization.strobe_plot import StrobePlotWidget
    from src.math.strobe_system import strobe_generator
    
    print("✅ Strobe system imported successfully")
    
    class StrobeTestWindow(QMainWindow):
        """Test window for strobe system."""
        
        def __init__(self):
            super().__init__()
            self.setWindowTitle("SignalAnalyzer - Тест системы стробов")
            self.setGeometry(100, 100, 1400, 900)
            
            self._setup_ui()
            self._test_strobe_generation()
        
        def _setup_ui(self):
            """Setup the test UI."""
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QVBoxLayout(central_widget)
            
            # Title
            title = QLabel("""
            <div style='text-align: center; padding: 20px;'>
                <h1>🎯 Тест системы стробов SignalAnalyzer</h1>
                <h2>Генерация и визуализация стробов с лучами</h2>
            </div>
            """)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title)
            
            # Test buttons
            button_layout = QVBoxLayout()
            
            self.test_btn = QPushButton("Генерировать тестовый строб (3 луча)")
            self.test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.test_btn.clicked.connect(self.generate_test_strobe)
            button_layout.addWidget(self.test_btn)
            
            # Status
            self.status_label = QLabel("Готов к тестированию системы стробов")
            self.status_label.setStyleSheet("""
                padding: 15px;
                background-color: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            """)
            button_layout.addWidget(self.status_label)
            
            layout.addLayout(button_layout)
            
            # Strobe configuration widget
            self.strobe_config = StrobeConfigWidget()
            layout.addWidget(self.strobe_config)
            
            # Strobe plot widget
            self.strobe_plot = StrobePlotWidget()
            layout.addWidget(self.strobe_plot)
            
            # Connect signals
            self.strobe_config.strobe_generated.connect(self.strobe_plot.plot_strobe)
        
        def _test_strobe_generation(self):
            """Test strobe generation."""
            self.status_label.setText("✅ Система стробов готова к тестированию")
        
        def generate_test_strobe(self):
            """Generate test strobe."""
            try:
                # Generate test strobe
                data, metadata = strobe_generator.create_test_strobe()
                
                # Plot the strobe
                self.strobe_plot.plot_strobe(data, metadata)
                
                self.status_label.setText(f"""
                ✅ Тестовый строб сгенерирован успешно!
                📊 Данные: {len(data)} точек
                🎯 Лучей: {metadata.get('num_rays', 0)}
                📏 Длина: {metadata.get('total_length', 0)} точек
                🔧 Частота дискретизации: {metadata.get('sample_rate', 0):.0f} Гц
                """)
                
                # Print detailed info
                print(f"\n🎯 Тестовый строб сгенерирован:")
                print(f"   📊 Общая длина: {len(data)} точек")
                print(f"   🎯 Количество лучей: {metadata.get('num_rays', 0)}")
                print(f"   📏 Точек на луч: {metadata.get('points_per_ray', 0)}")
                print(f"   🔧 Частота дискретизации: {metadata.get('sample_rate', 0):.0f} Гц")
                
                if 'rays' in metadata:
                    for i, ray in enumerate(metadata['rays']):
                        print(f"\n   Луч {i}:")
                        print(f"     🎵 Тип сигнала: {ray.get('signal_type', 'unknown')}")
                        print(f"     📡 Частота: {ray.get('frequency', 0):.1f} Гц")
                        print(f"     📊 Амплитуда: {ray.get('amplitude', 0):.2f} В")
                        print(f"     📍 Фаза: {np.degrees(ray.get('phase', 0)):.1f}°")
                        print(f"     📏 Длина данных: {ray.get('data_length', 0)} точек")
                        print(f"     🎯 Индексы: {ray.get('start_index', 0)}-{ray.get('end_index', 0)}")
                
                print(f"\n🎨 Визуализация:")
                print(f"   📈 Основной график: все лучи")
                print(f"   📊 FFT: частотная область")
                print(f"   🎯 Выбранный луч: детальный вид")
                print(f"   📍 Фаза: фазовые характеристики")
                print(f"   🌈 Спектрограмма: время-частота")
                
                # Save strobe
                strobe_generator.save_strobe("test_strobe.json", data, metadata)
                print(f"\n💾 Строб сохранен: test_strobe.json")
                
            except Exception as e:
                self.status_label.setText(f"❌ Ошибка: {str(e)}")
                print(f"❌ Ошибка генерации тестового строба: {e}")
    
    # Create and show the test window
    app = QApplication(sys.argv)
    window = StrobeTestWindow()
    window.show()
    
    print("✅ Тестовое окно системы стробов создано")
    print("\n🎯 Что можно протестировать:")
    print("  • Генерация тестового строба из 3 лучей")
    print("  • Конфигурация параметров лучей")
    print("  • Визуализация стробов в реальном времени")
    print("  • FFT анализ и спектрограмма")
    print("  • Сохранение и загрузка стробов")
    print("  • Различные типы сигналов и шумов")
    
    print("\n🚀 Система стробов готова к тестированию!")
    print("Нажмите кнопку для генерации тестового строба")
    
    # Run the application
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"❌ Error importing strobe system: {e}")
    print("Make sure all dependencies are installed:")
    print("  py -m pip install PyQt6 matplotlib numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Strobe system test failed: {e}")
    sys.exit(1)
