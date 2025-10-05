"""Визуализация стробов с лучами."""

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class StrobePlotWidget(QWidget):
    """Виджет для отображения стробов с лучами."""
    
    # Сигналы
    plot_updated = pyqtSignal(dict)  # Emitted when plot is updated
    
    def __init__(self, parent=None):
        """Инициализация виджета."""
        super().__init__(parent)
        self.strobe_data = None
        self.strobe_metadata = None
        self._setup_ui()
        self._setup_plot()
        logger.info("Виджет визуализации стробов инициализирован")
    
    def _setup_ui(self):
        """Настройка интерфейса."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Панель управления
        control_layout = QHBoxLayout()
        
        # Кнопки
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_plot)
        control_layout.addWidget(self.clear_btn)
        
        # Выбор луча для отображения
        control_layout.addWidget(QLabel("Луч:"))
        self.ray_combo = QComboBox()
        self.ray_combo.addItems(["Все лучи", "Луч 0", "Луч 1", "Луч 2"])
        self.ray_combo.currentTextChanged.connect(self.update_display)
        control_layout.addWidget(self.ray_combo)
        
        # Масштаб
        control_layout.addWidget(QLabel("Масштаб:"))
        self.scale_spinbox = QSpinBox()
        self.scale_spinbox.setRange(1, 1000)
        self.scale_spinbox.setValue(100)
        self.scale_spinbox.setSuffix("%")
        self.scale_spinbox.valueChanged.connect(self.update_display)
        control_layout.addWidget(self.scale_spinbox)
        
        control_layout.addStretch()
        
        # Статус
        self.status_label = QLabel("Готов к отображению")
        control_layout.addWidget(self.status_label)
        
        layout.addLayout(control_layout)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
    
    def _setup_plot(self):
        """Настройка matplotlib plot."""
        # Очищаем фигуру
        self.figure.clear()
        
        # Создаем subplots
        gs = GridSpec(3, 2, figure=self.figure, hspace=0.3, wspace=0.3)
        
        # Основной график - все лучи
        self.ax_main = self.figure.add_subplot(gs[0, :])
        self.ax_main.set_title("Строб - все лучи", fontsize=14, fontweight='bold')
        self.ax_main.set_xlabel("Время (индексы)")
        self.ax_main.set_ylabel("Амплитуда")
        self.ax_main.grid(True, alpha=0.3)
        
        # FFT основного сигнала
        self.ax_fft = self.figure.add_subplot(gs[1, 0])
        self.ax_fft.set_title("FFT - все лучи", fontsize=12)
        self.ax_fft.set_xlabel("Частота (индексы)")
        self.ax_fft.set_ylabel("Амплитуда")
        self.ax_fft.grid(True, alpha=0.3)
        
        # Выбранный луч
        self.ax_ray = self.figure.add_subplot(gs[1, 1])
        self.ax_ray.set_title("Выбранный луч", fontsize=12)
        self.ax_ray.set_xlabel("Время (индексы)")
        self.ax_ray.set_ylabel("Амплитуда")
        self.ax_ray.grid(True, alpha=0.3)
        
        # Фаза
        self.ax_phase = self.figure.add_subplot(gs[2, 0])
        self.ax_phase.set_title("Фаза", fontsize=12)
        self.ax_phase.set_xlabel("Время (индексы)")
        self.ax_phase.set_ylabel("Фаза (рад)")
        self.ax_phase.grid(True, alpha=0.3)
        
        # Спектрограмма
        self.ax_spectro = self.figure.add_subplot(gs[2, 1])
        self.ax_spectro.set_title("Спектрограмма", fontsize=12)
        self.ax_spectro.set_xlabel("Время")
        self.ax_spectro.set_ylabel("Частота")
        self.ax_spectro.grid(True, alpha=0.3)
        
        # Инициализируем пустые графики
        self.line_main, = self.ax_main.plot([], [], 'b-', linewidth=1, label='Строб')
        self.line_fft, = self.ax_fft.plot([], [], 'r-', linewidth=2, label='FFT')
        self.line_ray, = self.ax_ray.plot([], [], 'g-', linewidth=2, label='Луч')
        self.line_phase, = self.ax_phase.plot([], [], 'm-', linewidth=1, label='Фаза')
        
        # Легенды
        self.ax_main.legend()
        self.ax_fft.legend()
        self.ax_ray.legend()
        self.ax_phase.legend()
        
        # Рисуем
        self.canvas.draw()
    
    def plot_strobe(self, data: np.ndarray, metadata: dict):
        """Отобразить строб."""
        try:
            self.strobe_data = data
            self.strobe_metadata = metadata
            
            # Обновляем комбобокс лучей
            self._update_ray_combo()
            
            # Отображаем данные
            self.update_display()
            
            self.status_label.setText(f"Строб отображен: {len(data)} точек, {metadata.get('num_rays', 0)} лучей")
            
            # Эмитируем сигнал
            self.plot_updated.emit(metadata)
            
            logger.info(f"Строб отображен: {metadata.get('strobe_id', 'unknown')}")
            
        except Exception as e:
            self.status_label.setText(f"Ошибка отображения: {str(e)}")
            logger.error(f"Ошибка отображения строба: {e}")
    
    def _update_ray_combo(self):
        """Обновить комбобокс лучей."""
        self.ray_combo.clear()
        self.ray_combo.addItem("Все лучи")
        
        if self.strobe_metadata and 'rays' in self.strobe_metadata:
            for ray in self.strobe_metadata['rays']:
                self.ray_combo.addItem(f"Луч {ray['ray_id']}")
    
    def update_display(self):
        """Обновить отображение."""
        if self.strobe_data is None or self.strobe_metadata is None:
            return
        
        try:
            # Очищаем графики
            self.ax_main.clear()
            self.ax_fft.clear()
            self.ax_ray.clear()
            self.ax_phase.clear()
            self.ax_spectro.clear()
            
            # Получаем выбранный луч
            selected_ray = self.ray_combo.currentText()
            ray_index = None
            if selected_ray != "Все лучи":
                ray_index = int(selected_ray.split()[-1])
            
            # Отображаем основной сигнал
            time_indices = np.arange(len(self.strobe_data))
            real_data = np.real(self.strobe_data)
            
            self.ax_main.plot(time_indices, real_data, 'b-', linewidth=1, label='Строб')
            
            # Добавляем разделители между лучами
            if 'rays' in self.strobe_metadata:
                for ray in self.strobe_metadata['rays']:
                    start_idx = ray.get('start_index', 0)
                    self.ax_main.axvline(x=start_idx, color='red', linestyle='--', alpha=0.5)
                    self.ax_main.text(start_idx, np.max(real_data) * 0.9, f"Луч {ray['ray_id']}", 
                                    rotation=90, fontsize=8)
            
            self.ax_main.set_title("Строб - все лучи", fontsize=14, fontweight='bold')
            self.ax_main.set_xlabel("Время (индексы)")
            self.ax_main.set_ylabel("Амплитуда")
            self.ax_main.grid(True, alpha=0.3)
            self.ax_main.legend()
            
            # FFT всего сигнала
            fft_data = np.fft.fft(self.strobe_data)
            freqs = np.fft.fftfreq(len(self.strobe_data))
            positive_freqs = freqs[:len(freqs)//2]
            positive_fft = np.abs(fft_data[:len(fft_data)//2])
            
            self.ax_fft.plot(positive_freqs, positive_fft, 'r-', linewidth=2, label='FFT')
            self.ax_fft.set_title("FFT - все лучи", fontsize=12)
            self.ax_fft.set_xlabel("Частота (нормализованная)")
            self.ax_fft.set_ylabel("Амплитуда")
            self.ax_fft.grid(True, alpha=0.3)
            self.ax_fft.legend()
            
            # Отображаем выбранный луч
            if ray_index is not None and 'rays' in self.strobe_metadata:
                ray_info = None
                for ray in self.strobe_metadata['rays']:
                    if ray['ray_id'] == ray_index:
                        ray_info = ray
                        break
                
                if ray_info:
                    start_idx = ray_info['start_index']
                    end_idx = ray_info['end_index']
                    ray_data = self.strobe_data[start_idx:end_idx]
                    ray_time = np.arange(len(ray_data))
                    
                    self.ax_ray.plot(ray_time, np.real(ray_data), 'g-', linewidth=2, label=f'Луч {ray_index}')
                    self.ax_ray.set_title(f"Луч {ray_index}", fontsize=12)
                    self.ax_ray.set_xlabel("Время (индексы)")
                    self.ax_ray.set_ylabel("Амплитуда")
                    self.ax_ray.grid(True, alpha=0.3)
                    self.ax_ray.legend()
                    
                    # Фаза выбранного луча
                    phase_data = np.angle(ray_data)
                    self.ax_phase.plot(ray_time, phase_data, 'm-', linewidth=1, label=f'Фаза луча {ray_index}')
                    self.ax_phase.set_title(f"Фаза луча {ray_index}", fontsize=12)
                    self.ax_phase.set_xlabel("Время (индексы)")
                    self.ax_phase.set_ylabel("Фаза (рад)")
                    self.ax_phase.grid(True, alpha=0.3)
                    self.ax_phase.legend()
            
            # Спектрограмма (простая реализация)
            if len(self.strobe_data) > 100:
                # Разбиваем на сегменты для спектрограммы
                segment_size = len(self.strobe_data) // 20
                spectrogram_data = []
                
                for i in range(0, len(self.strobe_data) - segment_size, segment_size // 2):
                    segment = self.strobe_data[i:i + segment_size]
                    fft_segment = np.fft.fft(segment)
                    spectrogram_data.append(np.abs(fft_segment[:segment_size//2]))
                
                if spectrogram_data:
                    spectrogram_array = np.array(spectrogram_data).T
                    im = self.ax_spectro.imshow(spectrogram_array, aspect='auto', origin='lower', cmap='viridis')
                    self.ax_spectro.set_title("Спектрограмма", fontsize=12)
                    self.ax_spectro.set_xlabel("Время")
                    self.ax_spectro.set_ylabel("Частота")
                    self.ax_spectro.grid(True, alpha=0.3)
            
            # Обновляем canvas
            self.canvas.draw()
            
        except Exception as e:
            self.status_label.setText(f"Ошибка обновления: {str(e)}")
            logger.error(f"Ошибка обновления отображения: {e}")
    
    def clear_plot(self):
        """Очистить графики."""
        # Очищаем данные
        self.strobe_data = None
        self.strobe_metadata = None
        
        # Очищаем графики
        self.ax_main.clear()
        self.ax_fft.clear()
        self.ax_ray.clear()
        self.ax_phase.clear()
        self.ax_spectro.clear()
        
        # Восстанавливаем заголовки и сетку
        self.ax_main.set_title("Строб - все лучи", fontsize=14, fontweight='bold')
        self.ax_main.set_xlabel("Время (индексы)")
        self.ax_main.set_ylabel("Амплитуда")
        self.ax_main.grid(True, alpha=0.3)
        
        self.ax_fft.set_title("FFT - все лучи", fontsize=12)
        self.ax_fft.set_xlabel("Частота (нормализованная)")
        self.ax_fft.set_ylabel("Амплитуда")
        self.ax_fft.grid(True, alpha=0.3)
        
        self.ax_ray.set_title("Выбранный луч", fontsize=12)
        self.ax_ray.set_xlabel("Время (индексы)")
        self.ax_ray.set_ylabel("Амплитуда")
        self.ax_ray.grid(True, alpha=0.3)
        
        self.ax_phase.set_title("Фаза", fontsize=12)
        self.ax_phase.set_xlabel("Время (индексы)")
        self.ax_phase.set_ylabel("Фаза (рад)")
        self.ax_phase.grid(True, alpha=0.3)
        
        self.ax_spectro.set_title("Спектрограмма", fontsize=12)
        self.ax_spectro.set_xlabel("Время")
        self.ax_spectro.set_ylabel("Частота")
        self.ax_spectro.grid(True, alpha=0.3)
        
        # Обновляем canvas
        self.canvas.draw()
        
        # Обновляем статус
        self.status_label.setText("Графики очищены")
        
        # Обновляем комбобокс
        self.ray_combo.clear()
        self.ray_combo.addItem("Все лучи")
        
        logger.info("Графики очищены")

