"""Система стробов с лучами для SignalAnalyzer."""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class NoiseType(Enum):
    """Типы шума."""
    GAUSSIAN_WHITE = "gaussian_white"
    GAUSSIAN_COLORED = "gaussian_colored"
    UNIFORM = "uniform"
    PINK = "pink"
    BROWN = "brown"


class ModulationType(Enum):
    """Типы модуляции."""
    AM = "am"  # Амплитудная модуляция
    FM = "fm"  # Частотная модуляция
    PM = "pm"  # Фазовая модуляция


@dataclass
class RayParameters:
    """Параметры луча."""
    ray_id: int = 0
    signal_type: str = "sine"  # sine, cosine, square, sawtooth, triangle, quadrature, modulated, pulse
    frequency: float = 1000.0  # Hz
    amplitude: float = 1.0     # V
    phase: float = 0.0         # радианы
    offset: float = 0.0        # DC смещение
    
    # Для квадратурного сигнала
    quadrature_phase: float = np.pi/2  # 90 градусов
    
    # Для модулированного сигнала
    modulation_type: ModulationType = ModulationType.AM
    modulation_frequency: float = 100.0
    modulation_depth: float = 0.5
    
    # Для импульсного сигнала
    pulse_width: float = 0.1   # доля периода
    rise_time: float = 0.01    # время нарастания
    
    # Дополнительные параметры
    harmonics: List[Tuple[float, float, float]] = None  # [(амплитуда, частота, фаза), ...]
    noise_level: float = 0.0
    noise_type: NoiseType = NoiseType.GAUSSIAN_WHITE
    
    def __post_init__(self):
        """Инициализация после создания."""
        if self.harmonics is None:
            self.harmonics = []


@dataclass
class StrobeParameters:
    """Параметры строба."""
    strobe_id: str = "default"
    total_length: int = 1024   # общая длина строба в точках
    num_rays: int = 3          # количество лучей
    points_per_ray: int = 1024 # точек на луч (2^n)
    sample_rate: float = 100000.0  # частота дискретизации Hz
    ray_parameters: List[RayParameters] = None
    
    def __post_init__(self):
        """Инициализация после создания."""
        if self.ray_parameters is None:
            self.ray_parameters = [RayParameters(ray_id=i) for i in range(self.num_rays)]


class StrobeGenerator:
    """Генератор стробов с лучами."""
    
    def __init__(self):
        """Инициализация генератора."""
        self.current_strobe = None
        self.current_data = None
        logger.info("Генератор стробов инициализирован")
    
    def generate_strobe(self, params: StrobeParameters) -> Tuple[np.ndarray, Dict]:
        """
        Генерировать строб с лучами.
        
        Args:
            params: Параметры строба
            
        Returns:
            Tuple (data_array, metadata_dict)
        """
        try:
            # Создаем массив данных
            data = np.zeros(params.total_length, dtype=np.complex128)
            metadata = {
                'strobe_id': params.strobe_id,
                'total_length': params.total_length,
                'num_rays': params.num_rays,
                'points_per_ray': params.points_per_ray,
                'sample_rate': params.sample_rate,
                'rays': []
            }
            
            # Генерируем каждый луч
            for ray_idx, ray_params in enumerate(params.ray_parameters):
                ray_data = self._generate_ray(ray_params, params.points_per_ray, params.sample_rate)
                
                # Размещаем луч в стробах
                start_idx = ray_idx * params.points_per_ray
                end_idx = start_idx + params.points_per_ray
                
                if end_idx <= params.total_length:
                    data[start_idx:end_idx] = ray_data
                
                # Сохраняем метаданные луча
                ray_meta = {
                    'ray_id': ray_params.ray_id,
                    'signal_type': ray_params.signal_type,
                    'frequency': ray_params.frequency,
                    'amplitude': ray_params.amplitude,
                    'phase': ray_params.phase,
                    'start_index': start_idx,
                    'end_index': end_idx,
                    'data_length': len(ray_data)
                }
                metadata['rays'].append(ray_meta)
            
            # Сохраняем текущий строб
            self.current_strobe = params
            self.current_data = data
            
            logger.info(f"Сгенерирован строб: {params.strobe_id}, "
                       f"лучей: {params.num_rays}, "
                       f"точек: {params.total_length}")
            
            return data, metadata
            
        except Exception as e:
            logger.error(f"Ошибка генерации строба: {e}")
            raise
    
    def _generate_ray(self, ray_params: RayParameters, points: int, sample_rate: float) -> np.ndarray:
        """Генерировать данные одного луча."""
        # Создаем временную шкалу
        duration = points / sample_rate
        time = np.linspace(0, duration, points, endpoint=False)
        
        # Генерируем базовый сигнал
        if ray_params.signal_type == "sine":
            signal = ray_params.amplitude * np.sin(2 * np.pi * ray_params.frequency * time + ray_params.phase)
        elif ray_params.signal_type == "cosine":
            signal = ray_params.amplitude * np.cos(2 * np.pi * ray_params.frequency * time + ray_params.phase)
        elif ray_params.signal_type == "square":
            signal = self._generate_square_wave(time, ray_params)
        elif ray_params.signal_type == "sawtooth":
            signal = self._generate_sawtooth_wave(time, ray_params)
        elif ray_params.signal_type == "triangle":
            signal = self._generate_triangle_wave(time, ray_params)
        elif ray_params.signal_type == "quadrature":
            signal = self._generate_quadrature_signal(time, ray_params)
        elif ray_params.signal_type == "modulated":
            signal = self._generate_modulated_signal(time, ray_params)
        elif ray_params.signal_type == "pulse":
            signal = self._generate_pulse_signal(time, ray_params)
        else:
            signal = ray_params.amplitude * np.sin(2 * np.pi * ray_params.frequency * time + ray_params.phase)
        
        # Добавляем гармоники
        if ray_params.harmonics:
            for amp, freq, phase in ray_params.harmonics:
                harmonic = amp * np.sin(2 * np.pi * freq * time + phase)
                signal += harmonic
        
        # Добавляем шум
        if ray_params.noise_level > 0:
            noise = self._generate_noise(points, ray_params.noise_type, ray_params.noise_level)
            signal += noise
        
        # Добавляем DC смещение
        signal += ray_params.offset
        
        return signal.astype(np.complex128)
    
    def _generate_square_wave(self, time: np.ndarray, params: RayParameters) -> np.ndarray:
        """Генерировать прямоугольный сигнал."""
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        
        signal = np.zeros_like(time)
        for i, t in enumerate(phase_time):
            if t < params.pulse_width * period:
                signal[i] = params.amplitude
            else:
                signal[i] = -params.amplitude
        
        return signal
    
    def _generate_sawtooth_wave(self, time: np.ndarray, params: RayParameters) -> np.ndarray:
        """Генерировать пилообразный сигнал."""
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        return params.amplitude * (2 * phase_time / period - 1)
    
    def _generate_triangle_wave(self, time: np.ndarray, params: RayParameters) -> np.ndarray:
        """Генерировать треугольный сигнал."""
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        
        signal = np.zeros_like(time)
        half_period = period / 2
        
        for i, t in enumerate(phase_time):
            if t < half_period:
                signal[i] = params.amplitude * (2 * t / half_period - 1)
            else:
                signal[i] = params.amplitude * (3 - 2 * t / half_period)
        
        return signal
    
    def _generate_quadrature_signal(self, time: np.ndarray, params: RayParameters) -> np.ndarray:
        """Генерировать квадратурный сигнал (I + jQ)."""
        I = params.amplitude * np.cos(2 * np.pi * params.frequency * time + params.phase)
        Q = params.amplitude * np.sin(2 * np.pi * params.frequency * time + params.phase + params.quadrature_phase)
        return I + 1j * Q
    
    def _generate_modulated_signal(self, time: np.ndarray, params: RayParameters) -> np.ndarray:
        """Генерировать модулированный сигнал."""
        carrier = params.amplitude * np.sin(2 * np.pi * params.frequency * time + params.phase)
        
        if params.modulation_type == ModulationType.AM:
            # Амплитудная модуляция
            modulation = 1 + params.modulation_depth * np.sin(2 * np.pi * params.modulation_frequency * time)
            return carrier * modulation
        elif params.modulation_type == ModulationType.FM:
            # Частотная модуляция
            mod_phase = 2 * np.pi * params.modulation_depth * np.sin(2 * np.pi * params.modulation_frequency * time)
            return params.amplitude * np.sin(2 * np.pi * params.frequency * time + mod_phase + params.phase)
        elif params.modulation_type == ModulationType.PM:
            # Фазовая модуляция
            mod_phase = params.modulation_depth * np.sin(2 * np.pi * params.modulation_frequency * time)
            return params.amplitude * np.sin(2 * np.pi * params.frequency * time + params.phase + mod_phase)
        else:
            return carrier
    
    def _generate_pulse_signal(self, time: np.ndarray, params: RayParameters) -> np.ndarray:
        """Генерировать импульсный сигнал."""
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        
        signal = np.zeros_like(time)
        pulse_width = params.pulse_width * period
        rise_samples = int(params.rise_time * len(time) / (len(time) * period))
        
        for i, t in enumerate(phase_time):
            if t < pulse_width:
                if rise_samples > 0 and i < rise_samples:
                    # Нарастающий фронт
                    signal[i] = params.amplitude * i / rise_samples
                else:
                    signal[i] = params.amplitude
            else:
                signal[i] = 0
        
        return signal
    
    def _generate_noise(self, points: int, noise_type: NoiseType, level: float) -> np.ndarray:
        """Генерировать шум."""
        if noise_type == NoiseType.GAUSSIAN_WHITE:
            return level * np.random.normal(0, 1, points)
        elif noise_type == NoiseType.UNIFORM:
            return level * (np.random.uniform(-1, 1, points))
        elif noise_type == NoiseType.GAUSSIAN_COLORED:
            # Цветной гауссов шум (простая реализация)
            white_noise = np.random.normal(0, 1, points)
            # Простой фильтр низких частот
            colored_noise = np.convolve(white_noise, np.ones(5)/5, mode='same')
            return level * colored_noise
        else:
            return level * np.random.normal(0, 1, points)
    
    def create_test_strobe(self) -> Tuple[np.ndarray, Dict]:
        """Создать тестовый строб из 3 лучей по заданным параметрам."""
        # Параметры тестового строба
        strobe_params = StrobeParameters(
            strobe_id="test_3_rays",
            total_length=3072,  # 3 луча по 1024 точки
            num_rays=3,
            points_per_ray=1024,
            sample_rate=100000.0
        )
        
        # Луч 0: сумма синусов с периодом 300 и 200 точек
        ray0 = RayParameters(
            ray_id=0,
            signal_type="sine",
            frequency=100000/300,  # период 300 точек
            amplitude=1.0,
            phase=0.0,
            harmonics=[
                (0.7, 100000/200, np.radians(30))  # второй синус с периодом 200 точек
            ],
            noise_level=0.2,
            noise_type=NoiseType.GAUSSIAN_WHITE
        )
        
        # Луч 1: сумма синусов с периодом 250 и 150 точек
        ray1 = RayParameters(
            ray_id=1,
            signal_type="sine",
            frequency=100000/250,  # период 250 точек
            amplitude=1.0,
            phase=0.0,
            harmonics=[
                (0.7, 100000/150, np.radians(40))  # второй синус с периодом 150 точек
            ],
            noise_level=0.2,
            noise_type=NoiseType.GAUSSIAN_WHITE
        )
        
        # Луч 2: сумма синусов с периодом 200 и 100 точек
        ray2 = RayParameters(
            ray_id=2,
            signal_type="sine",
            frequency=100000/200,  # период 200 точек
            amplitude=1.0,
            phase=0.0,
            harmonics=[
                (0.7, 100000/100, np.radians(50))  # второй синус с периодом 100 точек
            ],
            noise_level=0.2,
            noise_type=NoiseType.GAUSSIAN_WHITE
        )
        
        strobe_params.ray_parameters = [ray0, ray1, ray2]
        
        return self.generate_strobe(strobe_params)
    
    def save_strobe(self, filename: str, data: np.ndarray, metadata: Dict) -> bool:
        """Сохранить строб в файл."""
        try:
            # Сохраняем данные
            np.save(filename.replace('.json', '.npy'), data)
            
            # Сохраняем метаданные
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Строб сохранен: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения строба: {e}")
            return False
    
    def load_strobe(self, filename: str) -> Tuple[Optional[np.ndarray], Optional[Dict]]:
        """Загрузить строб из файла."""
        try:
            # Загружаем данные
            data = np.load(filename.replace('.json', '.npy'))
            
            # Загружаем метаданные
            with open(filename, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"Строб загружен: {filename}")
            return data, metadata
            
        except Exception as e:
            logger.error(f"Ошибка загрузки строба: {e}")
            return None, None


# Глобальный экземпляр генератора стробов
strobe_generator = StrobeGenerator()

