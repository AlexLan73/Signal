"""Виджет для работы со стробами и лучами."""

import numpy as np
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, 
    QPushButton, QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox,
    QFormLayout, QLineEdit, QTextEdit, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..math.strobe_system import (
    StrobeGenerator, StrobeParameters, RayParameters, 
    NoiseType, ModulationType
)
from ..gui.localization import tr
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class RayConfigWidget(QWidget):
    """Виджет конфигурации луча."""
    
    parameters_changed = pyqtSignal(int, dict)  # ray_id, parameters
    
    def __init__(self, ray_id: int = 0, parent=None):
        super().__init__(parent)
        self.ray_id = ray_id
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Настройка интерфейса."""
        layout = QVBoxLayout(self)
        
        # Заголовок луча
        title = QLabel(f"Луч {self.ray_id}")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #2196F3;")
        layout.addWidget(title)
        
        # Основные параметры
        main_group = QGroupBox("Основные параметры")
        main_layout = QFormLayout(main_group)
        
        # Тип сигнала
        self.signal_type_combo = QComboBox()
        self.signal_type_combo.addItems([
            "sine", "cosine", "square", "sawtooth", "triangle",
            "quadrature", "modulated", "pulse"
        ])
        main_layout.addRow("Тип сигнала:", self.signal_type_combo)
        
        # Частота
        self.frequency_spinbox = QDoubleSpinBox()
        self.frequency_spinbox.setRange(0.1, 100000.0)
        self.frequency_spinbox.setValue(1000.0)
        self.frequency_spinbox.setSuffix(" Гц")
        main_layout.addRow("Частота:", self.frequency_spinbox)
        
        # Амплитуда
        self.amplitude_spinbox = QDoubleSpinBox()
        self.amplitude_spinbox.setRange(0.0, 10.0)
        self.amplitude_spinbox.setValue(1.0)
        self.amplitude_spinbox.setSuffix(" В")
        main_layout.addRow("Амплитуда:", self.amplitude_spinbox)
        
        # Фаза
        self.phase_spinbox = QDoubleSpinBox()
        self.phase_spinbox.setRange(-360, 360)
        self.phase_spinbox.setValue(0.0)
        self.phase_spinbox.setSuffix(" град")
        main_layout.addRow("Фаза:", self.phase_spinbox)
        
        # DC смещение
        self.offset_spinbox = QDoubleSpinBox()
        self.offset_spinbox.setRange(-5.0, 5.0)
        self.offset_spinbox.setValue(0.0)
        self.offset_spinbox.setSuffix(" В")
        main_layout.addRow("DC смещение:", self.offset_spinbox)
        
        layout.addWidget(main_group)
        
        # Гармоники
        harmonics_group = QGroupBox("Гармоники")
        harmonics_layout = QVBoxLayout(harmonics_group)
        
        self.harmonics_text = QTextEdit()
        self.harmonics_text.setMaximumHeight(80)
        self.harmonics_text.setPlaceholderText(
            "Формат: амплитуда,частота,фаза\n"
            "Пример: 0.7,2000,30\n"
            "Несколько гармоник - по одной на строку"
        )
        harmonics_layout.addWidget(self.harmonics_text)
        
        layout.addWidget(harmonics_group)
        
        # Шум
        noise_group = QGroupBox("Шум")
        noise_layout = QFormLayout(noise_group)
        
        self.noise_enabled = QCheckBox("Включить шум")
        noise_layout.addRow(self.noise_enabled)
        
        self.noise_type_combo = QComboBox()
        for noise_type in NoiseType:
            self.noise_type_combo.addItem(noise_type.value)
        noise_layout.addRow("Тип шума:", self.noise_type_combo)
        
        self.noise_level_spinbox = QDoubleSpinBox()
        self.noise_level_spinbox.setRange(0.0, 1.0)
        self.noise_level_spinbox.setValue(0.0)
        self.noise_level_spinbox.setSingleStep(0.1)
        noise_layout.addRow("Уровень шума:", self.noise_level_spinbox)
        
        layout.addWidget(noise_group)
        
        # Параметры модуляции
        modulation_group = QGroupBox("Модуляция")
        modulation_layout = QFormLayout(modulation_group)
        
        self.modulation_type_combo = QComboBox()
        for mod_type in ModulationType:
            self.modulation_type_combo.addItem(mod_type.value)
        modulation_layout.addRow("Тип модуляции:", self.modulation_type_combo)
        
        self.modulation_freq_spinbox = QDoubleSpinBox()
        self.modulation_freq_spinbox.setRange(1.0, 10000.0)
        self.modulation_freq_spinbox.setValue(100.0)
        self.modulation_freq_spinbox.setSuffix(" Гц")
        modulation_layout.addRow("Частота модуляции:", self.modulation_freq_spinbox)
        
        self.modulation_depth_spinbox = QDoubleSpinBox()
        self.modulation_depth_spinbox.setRange(0.0, 1.0)
        self.modulation_depth_spinbox.setValue(0.5)
        modulation_layout.addRow("Глубина модуляции:", self.modulation_depth_spinbox)
        
        layout.addWidget(modulation_group)
    
    def _connect_signals(self):
        """Подключение сигналов."""
        self.signal_type_combo.currentTextChanged.connect(self._emit_changes)
        self.frequency_spinbox.valueChanged.connect(self._emit_changes)
        self.amplitude_spinbox.valueChanged.connect(self._emit_changes)
        self.phase_spinbox.valueChanged.connect(self._emit_changes)
        self.offset_spinbox.valueChanged.connect(self._emit_changes)
        self.harmonics_text.textChanged.connect(self._emit_changes)
        self.noise_enabled.toggled.connect(self._emit_changes)
        self.noise_type_combo.currentTextChanged.connect(self._emit_changes)
        self.noise_level_spinbox.valueChanged.connect(self._emit_changes)
        self.modulation_type_combo.currentTextChanged.connect(self._emit_changes)
        self.modulation_freq_spinbox.valueChanged.connect(self._emit_changes)
        self.modulation_depth_spinbox.valueChanged.connect(self._emit_changes)
    
    def _emit_changes(self):
        """Эмиссия сигнала об изменении параметров."""
        params = self.get_parameters()
        self.parameters_changed.emit(self.ray_id, params)
    
    def get_parameters(self) -> Dict:
        """Получить параметры луча."""
        # Парсинг гармоник
        harmonics = []
        harmonics_text = self.harmonics_text.toPlainText().strip()
        if harmonics_text:
            for line in harmonics_text.split('\n'):
                line = line.strip()
                if line:
                    try:
                        parts = line.split(',')
                        if len(parts) == 3:
                            amp, freq, phase = map(float, parts)
                            harmonics.append((amp, freq, np.radians(phase)))
                    except ValueError:
                        continue
        
        return {
            'signal_type': self.signal_type_combo.currentText(),
            'frequency': self.frequency_spinbox.value(),
            'amplitude': self.amplitude_spinbox.value(),
            'phase': np.radians(self.phase_spinbox.value()),
            'offset': self.offset_spinbox.value(),
            'harmonics': harmonics,
            'noise_enabled': self.noise_enabled.isChecked(),
            'noise_type': NoiseType(self.noise_type_combo.currentText()),
            'noise_level': self.noise_level_spinbox.value() if self.noise_enabled.isChecked() else 0.0,
            'modulation_type': ModulationType(self.modulation_type_combo.currentText()),
            'modulation_frequency': self.modulation_freq_spinbox.value(),
            'modulation_depth': self.modulation_depth_spinbox.value()
        }
    
    def set_parameters(self, params: Dict):
        """Установить параметры луча."""
        self.signal_type_combo.setCurrentText(params.get('signal_type', 'sine'))
        self.frequency_spinbox.setValue(params.get('frequency', 1000.0))
        self.amplitude_spinbox.setValue(params.get('amplitude', 1.0))
        self.phase_spinbox.setValue(np.degrees(params.get('phase', 0.0)))
        self.offset_spinbox.setValue(params.get('offset', 0.0))
        
        # Установка гармоник
        harmonics_text = ""
        for amp, freq, phase in params.get('harmonics', []):
            harmonics_text += f"{amp},{freq},{np.degrees(phase)}\n"
        self.harmonics_text.setPlainText(harmonics_text.strip())
        
        # Установка шума
        noise_enabled = params.get('noise_enabled', False)
        self.noise_enabled.setChecked(noise_enabled)
        self.noise_type_combo.setCurrentText(params.get('noise_type', NoiseType.GAUSSIAN_WHITE).value)
        self.noise_level_spinbox.setValue(params.get('noise_level', 0.0))
        
        # Установка модуляции
        self.modulation_type_combo.setCurrentText(params.get('modulation_type', ModulationType.AM).value)
        self.modulation_freq_spinbox.setValue(params.get('modulation_frequency', 100.0))
        self.modulation_depth_spinbox.setValue(params.get('modulation_depth', 0.5))


class StrobeConfigWidget(QWidget):
    """Виджет конфигурации строба."""
    
    strobe_generated = pyqtSignal(np.ndarray, dict)  # data, metadata
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.strobe_generator = StrobeGenerator()
        self.ray_widgets = []
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Настройка интерфейса."""
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel("Конфигурация строба")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Общие параметры строба
        strobe_group = QGroupBox("Общие параметры строба")
        strobe_layout = QFormLayout(strobe_group)
        
        # ID строба
        self.strobe_id_edit = QLineEdit("test_strobe")
        strobe_layout.addRow("ID строба:", self.strobe_id_edit)
        
        # Общая длина
        self.total_length_spinbox = QSpinBox()
        self.total_length_spinbox.setRange(256, 65536)
        self.total_length_spinbox.setValue(3072)
        strobe_layout.addRow("Общая длина (точек):", self.total_length_spinbox)
        
        # Количество лучей
        self.num_rays_spinbox = QSpinBox()
        self.num_rays_spinbox.setRange(1, 16)
        self.num_rays_spinbox.setValue(3)
        self.num_rays_spinbox.valueChanged.connect(self._update_ray_widgets)
        strobe_layout.addRow("Количество лучей:", self.num_rays_spinbox)
        
        # Точки на луч
        self.points_per_ray_spinbox = QSpinBox()
        self.points_per_ray_spinbox.setRange(64, 16384)
        self.points_per_ray_spinbox.setValue(1024)
        strobe_layout.addRow("Точек на луч:", self.points_per_ray_spinbox)
        
        # Частота дискретизации
        self.sample_rate_spinbox = QDoubleSpinBox()
        self.sample_rate_spinbox.setRange(1000.0, 1000000.0)
        self.sample_rate_spinbox.setValue(100000.0)
        self.sample_rate_spinbox.setSuffix(" Гц")
        strobe_layout.addRow("Частота дискретизации:", self.sample_rate_spinbox)
        
        layout.addWidget(strobe_group)
        
        # Вкладки лучей
        self.ray_tabs = QTabWidget()
        layout.addWidget(self.ray_tabs)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("Генерировать строб")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_strobe)
        button_layout.addWidget(self.generate_btn)
        
        self.test_btn = QPushButton("Тестовый строб (3 луча)")
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.test_btn.clicked.connect(self.generate_test_strobe)
        button_layout.addWidget(self.test_btn)
        
        self.save_btn = QPushButton("Сохранить строб")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.save_btn.clicked.connect(self.save_strobe)
        button_layout.addWidget(self.save_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Статус
        self.status_label = QLabel("Готов к генерации строба")
        self.status_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(self.status_label)
        
        # Инициализируем виджеты лучей
        self._update_ray_widgets()
    
    def _connect_signals(self):
        """Подключение сигналов."""
        self.strobe_id_edit.textChanged.connect(self._update_status)
        self.total_length_spinbox.valueChanged.connect(self._update_status)
        self.num_rays_spinbox.valueChanged.connect(self._update_status)
        self.points_per_ray_spinbox.valueChanged.connect(self._update_status)
        self.sample_rate_spinbox.valueChanged.connect(self._update_status)
    
    def _update_ray_widgets(self):
        """Обновить виджеты лучей."""
        num_rays = self.num_rays_spinbox.value()
        
        # Удаляем старые вкладки
        self.ray_tabs.clear()
        self.ray_widgets.clear()
        
        # Создаем новые вкладки
        for i in range(num_rays):
            ray_widget = RayConfigWidget(ray_id=i)
            ray_widget.parameters_changed.connect(self._on_ray_parameters_changed)
            self.ray_widgets.append(ray_widget)
            self.ray_tabs.addTab(ray_widget, f"Луч {i}")
        
        self._update_status()
    
    def _on_ray_parameters_changed(self, ray_id: int, parameters: Dict):
        """Обработка изменения параметров луча."""
        self._update_status()
    
    def _update_status(self):
        """Обновить статус."""
        total_length = self.total_length_spinbox.value()
        num_rays = self.num_rays_spinbox.value()
        points_per_ray = self.points_per_ray_spinbox.value()
        
        self.status_label.setText(
            f"Строб: {self.strobe_id_edit.text()}, "
            f"лучей: {num_rays}, "
            f"точек: {total_length}, "
            f"на луч: {points_per_ray}"
        )
    
    def get_strobe_parameters(self) -> StrobeParameters:
        """Получить параметры строба."""
        # Собираем параметры лучей
        ray_parameters = []
        for i, ray_widget in enumerate(self.ray_widgets):
            ray_params = ray_widget.get_parameters()
            ray_parameters.append(RayParameters(ray_id=i, **ray_params))
        
        return StrobeParameters(
            strobe_id=self.strobe_id_edit.text(),
            total_length=self.total_length_spinbox.value(),
            num_rays=self.num_rays_spinbox.value(),
            points_per_ray=self.points_per_ray_spinbox.value(),
            sample_rate=self.sample_rate_spinbox.value(),
            ray_parameters=ray_parameters
        )
    
    def generate_strobe(self):
        """Генерировать строб."""
        try:
            params = self.get_strobe_parameters()
            data, metadata = self.strobe_generator.generate_strobe(params)
            
            self.status_label.setText(f"Строб сгенерирован: {len(data)} точек")
            self.strobe_generated.emit(data, metadata)
            
            logger.info(f"Строб сгенерирован: {params.strobe_id}")
            
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")
            logger.error(f"Ошибка генерации строба: {e}")
    
    def generate_test_strobe(self):
        """Генерировать тестовый строб."""
        try:
            data, metadata = self.strobe_generator.create_test_strobe()
            
            self.status_label.setText(f"Тестовый строб сгенерирован: {len(data)} точек")
            self.strobe_generated.emit(data, metadata)
            
            logger.info("Тестовый строб сгенерирован")
            
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")
            logger.error(f"Ошибка генерации тестового строба: {e}")
    
    def save_strobe(self):
        """Сохранить текущий строб."""
        try:
            if self.strobe_generator.current_data is None:
                self.status_label.setText("Нет данных для сохранения")
                return
            
            filename = f"strobe_{self.strobe_id_edit.text()}.json"
            success = self.strobe_generator.save_strobe(
                filename, 
                self.strobe_generator.current_data,
                self.strobe_generator.current_strobe.__dict__ if self.strobe_generator.current_strobe else {}
            )
            
            if success:
                self.status_label.setText(f"Строб сохранен: {filename}")
            else:
                self.status_label.setText("Ошибка сохранения")
                
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")
            logger.error(f"Ошибка сохранения строба: {e}")

