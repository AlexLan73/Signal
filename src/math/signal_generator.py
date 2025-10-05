"""Mathematical signal generator for SignalAnalyzer."""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class SignalType(Enum):
    """Types of mathematical signals."""
    SINE = "sine"
    COSINE = "cosine"
    SQUARE = "square"
    SAWTOOTH = "sawtooth"
    TRIANGLE = "triangle"
    NOISE = "noise"
    CHIRP = "chirp"
    PULSE = "pulse"
    COMPLEX = "complex"


@dataclass
class SignalParameters:
    """Parameters for signal generation."""
    frequency: float = 1000.0  # Hz
    amplitude: float = 1.0     # Volts
    phase: float = 0.0         # radians
    offset: float = 0.0        # DC offset
    sample_rate: float = 44100.0  # samples per second
    duration: float = 1.0      # seconds
    signal_type: SignalType = SignalType.SINE
    
    # Additional parameters for specific signal types
    duty_cycle: float = 0.5    # for square waves
    rise_time: float = 0.01    # for pulse waves
    noise_level: float = 0.1   # for noise signals
    chirp_start_freq: float = 100.0  # for chirp signals
    chirp_end_freq: float = 10000.0  # for chirp signals
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if self.frequency <= 0:
            raise ValueError("Frequency must be positive")
        if self.amplitude <= 0:
            raise ValueError("Amplitude must be positive")
        if self.sample_rate <= 0:
            raise ValueError("Sample rate must be positive")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not 0 <= self.duty_cycle <= 1:
            raise ValueError("Duty cycle must be between 0 and 1")


class SignalGenerator:
    """Mathematical signal generator."""
    
    def __init__(self):
        """Initialize the signal generator."""
        self.current_signal = None
        self.current_time = None
        logger.info("Signal generator initialized")
    
    def generate_signal(self, params: SignalParameters) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a mathematical signal based on parameters.
        
        Args:
            params: Signal parameters
            
        Returns:
            Tuple of (time_array, signal_array)
        """
        try:
            # Generate time vector
            samples = int(params.duration * params.sample_rate)
            time = np.linspace(0, params.duration, samples, endpoint=False)
            
            # Generate signal based on type
            if params.signal_type == SignalType.SINE:
                signal = self._generate_sine(time, params)
            elif params.signal_type == SignalType.COSINE:
                signal = self._generate_cosine(time, params)
            elif params.signal_type == SignalType.SQUARE:
                signal = self._generate_square(time, params)
            elif params.signal_type == SignalType.SAWTOOTH:
                signal = self._generate_sawtooth(time, params)
            elif params.signal_type == SignalType.TRIANGLE:
                signal = self._generate_triangle(time, params)
            elif params.signal_type == SignalType.NOISE:
                signal = self._generate_noise(time, params)
            elif params.signal_type == SignalType.CHIRP:
                signal = self._generate_chirp(time, params)
            elif params.signal_type == SignalType.PULSE:
                signal = self._generate_pulse(time, params)
            elif params.signal_type == SignalType.COMPLEX:
                signal = self._generate_complex(time, params)
            else:
                raise ValueError(f"Unknown signal type: {params.signal_type}")
            
            # Apply DC offset
            signal += params.offset
            
            # Store current signal
            self.current_signal = signal
            self.current_time = time
            
            logger.info(f"Generated {params.signal_type.value} signal: "
                       f"{params.frequency} Hz, {params.amplitude} V, "
                       f"{len(signal)} samples")
            
            return time, signal
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            raise
    
    def _generate_sine(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate sine wave signal."""
        return params.amplitude * np.sin(2 * np.pi * params.frequency * time + params.phase)
    
    def _generate_cosine(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate cosine wave signal."""
        return params.amplitude * np.cos(2 * np.pi * params.frequency * time + params.phase)
    
    def _generate_square(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate square wave signal."""
        # Create square wave using numpy
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        duty_samples = int(params.duty_cycle * period * params.sample_rate)
        
        signal = np.zeros_like(time)
        for i, t in enumerate(phase_time):
            if t < params.duty_cycle * period:
                signal[i] = params.amplitude
            else:
                signal[i] = -params.amplitude
        
        return signal
    
    def _generate_sawtooth(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate sawtooth wave signal."""
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        return params.amplitude * (2 * phase_time / period - 1)
    
    def _generate_triangle(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate triangle wave signal."""
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
    
    def _generate_noise(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate noise signal."""
        return params.amplitude * np.random.normal(0, params.noise_level, len(time))
    
    def _generate_chirp(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate chirp (frequency sweep) signal."""
        # Linear frequency sweep
        freq_sweep = params.chirp_start_freq + (
            params.chirp_end_freq - params.chirp_start_freq
        ) * time / params.duration
        
        # Generate chirp signal
        phase = 2 * np.pi * np.cumsum(freq_sweep) / params.sample_rate
        return params.amplitude * np.sin(phase + params.phase)
    
    def _generate_pulse(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate pulse signal."""
        period = 1.0 / params.frequency
        phase_time = (time + params.phase / (2 * np.pi * params.frequency)) % period
        
        signal = np.zeros_like(time)
        pulse_width = params.duty_cycle * period
        rise_samples = int(params.rise_time * params.sample_rate)
        
        for i, t in enumerate(phase_time):
            if t < pulse_width:
                if rise_samples > 0 and i < rise_samples:
                    # Rising edge
                    signal[i] = params.amplitude * i / rise_samples
                else:
                    signal[i] = params.amplitude
            else:
                signal[i] = 0
        
        return signal
    
    def _generate_complex(self, time: np.ndarray, params: SignalParameters) -> np.ndarray:
        """Generate complex signal (sum of multiple frequencies)."""
        # Generate multiple harmonics
        fundamental = params.frequency
        harmonics = [1, 2, 3, 5]  # Fundamental, 2nd, 3rd, 5th harmonics
        
        signal = np.zeros_like(time)
        for i, harmonic in enumerate(harmonics):
            freq = fundamental * harmonic
            amplitude = params.amplitude / harmonic  # Decreasing amplitude
            harmonic_signal = amplitude * np.sin(2 * np.pi * freq * time + params.phase)
            signal += harmonic_signal
        
        return signal
    
    def add_noise(self, signal: np.ndarray, noise_level: float = 0.1) -> np.ndarray:
        """
        Add noise to an existing signal.
        
        Args:
            signal: Input signal
            noise_level: Noise level (0-1)
            
        Returns:
            Signal with added noise
        """
        noise = np.random.normal(0, noise_level, len(signal))
        return signal + noise
    
    def apply_filter(self, signal: np.ndarray, filter_type: str = "lowpass", 
                    cutoff_freq: float = 1000.0) -> np.ndarray:
        """
        Apply a simple filter to the signal.
        
        Args:
            signal: Input signal
            filter_type: Type of filter ("lowpass", "highpass", "bandpass")
            cutoff_freq: Cutoff frequency
            
        Returns:
            Filtered signal
        """
        # Simple moving average filter (lowpass)
        if filter_type == "lowpass":
            window_size = int(self.current_time.shape[0] * cutoff_freq / (44100 / 2))
            if window_size < 3:
                window_size = 3
            
            filtered = np.convolve(signal, np.ones(window_size)/window_size, mode='same')
            return filtered
        
        # For other filter types, return original signal for now
        logger.warning(f"Filter type {filter_type} not implemented yet")
        return signal
    
    def get_signal_info(self) -> Dict:
        """Get information about the current signal."""
        if self.current_signal is None:
            return {"status": "No signal generated"}
        
        return {
            "status": "Signal available",
            "samples": len(self.current_signal),
            "duration": self.current_time[-1] if len(self.current_time) > 0 else 0,
            "max_value": np.max(self.current_signal),
            "min_value": np.min(self.current_signal),
            "rms_value": np.sqrt(np.mean(self.current_signal**2)),
            "peak_to_peak": np.max(self.current_signal) - np.min(self.current_signal)
        }
    
    def save_signal(self, filename: str) -> bool:
        """
        Save current signal to file.
        
        Args:
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.current_signal is None or self.current_time is None:
                logger.error("No signal to save")
                return False
            
            # Save as CSV
            data = np.column_stack((self.current_time, self.current_signal))
            np.savetxt(filename, data, delimiter=',', 
                      header='time,signal', comments='')
            
            logger.info(f"Signal saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving signal: {e}")
            return False


class SignalAnalyzer:
    """Signal analysis utilities."""
    
    @staticmethod
    def compute_fft(signal: np.ndarray, sample_rate: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT of signal.
        
        Args:
            signal: Input signal
            sample_rate: Sample rate
            
        Returns:
            Tuple of (frequencies, magnitude)
        """
        fft_result = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/sample_rate)
        
        # Only return positive frequencies
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(fft_result[:len(fft_result)//2])
        
        return positive_freqs, positive_fft
    
    @staticmethod
    def compute_spectral_density(signal: np.ndarray, sample_rate: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute power spectral density.
        
        Args:
            signal: Input signal
            sample_rate: Sample rate
            
        Returns:
            Tuple of (frequencies, power_spectral_density)
        """
        freqs, fft_mag = SignalAnalyzer.compute_fft(signal, sample_rate)
        psd = fft_mag**2 / len(signal)
        return freqs, psd
    
    @staticmethod
    def find_peaks(signal: np.ndarray, threshold: float = 0.1) -> List[int]:
        """
        Find peaks in signal.
        
        Args:
            signal: Input signal
            threshold: Peak detection threshold
            
        Returns:
            List of peak indices
        """
        peaks = []
        for i in range(1, len(signal) - 1):
            if (signal[i] > signal[i-1] and 
                signal[i] > signal[i+1] and 
                signal[i] > threshold):
                peaks.append(i)
        return peaks
    
    @staticmethod
    def compute_statistics(signal: np.ndarray) -> Dict:
        """
        Compute signal statistics.
        
        Args:
            signal: Input signal
            
        Returns:
            Dictionary of statistics
        """
        return {
            "mean": np.mean(signal),
            "std": np.std(signal),
            "rms": np.sqrt(np.mean(signal**2)),
            "peak_to_peak": np.max(signal) - np.min(signal),
            "crest_factor": np.max(np.abs(signal)) / np.sqrt(np.mean(signal**2)),
            "kurtosis": np.mean((signal - np.mean(signal))**4) / np.std(signal)**4,
            "skewness": np.mean((signal - np.mean(signal))**3) / np.std(signal)**3
        }


# Global signal generator instance
signal_generator = SignalGenerator()

