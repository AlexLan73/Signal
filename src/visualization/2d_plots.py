"""2D plotting with matplotlib integration for SignalAnalyzer."""

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # Use Qt5 backend for PyQt6 integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QDoubleSpinBox
from PyQt6.QtCore import Qt, pyqtSignal

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class Plot2DWidget(QWidget):
    """2D plotting widget with matplotlib integration."""
    
    # Signals
    plot_updated = pyqtSignal(dict)  # Emitted when plot is updated
    
    def __init__(self, parent=None):
        """Initialize the 2D plot widget."""
        super().__init__(parent)
        self._setup_ui()
        self._setup_plot()
        self._connect_signals()
        
        logger.info("2D Plot widget initialized")
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # Plot controls
        self.plot_btn = QPushButton("Plot Signal")
        self.plot_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        control_layout.addWidget(self.plot_btn)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
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
        control_layout.addWidget(self.clear_btn)
        
        # Grid toggle
        self.grid_btn = QPushButton("Toggle Grid")
        self.grid_btn.setCheckable(True)
        self.grid_btn.setChecked(True)
        control_layout.addWidget(self.grid_btn)
        
        control_layout.addStretch()
        
        # Signal parameters
        control_layout.addWidget(QLabel("Frequency:"))
        self.freq_spinbox = QDoubleSpinBox()
        self.freq_spinbox.setRange(0.1, 10000.0)
        self.freq_spinbox.setValue(1000.0)
        self.freq_spinbox.setSuffix(" Hz")
        control_layout.addWidget(self.freq_spinbox)
        
        control_layout.addWidget(QLabel("Amplitude:"))
        self.amp_spinbox = QDoubleSpinBox()
        self.amp_spinbox.setRange(0.1, 10.0)
        self.amp_spinbox.setValue(1.0)
        self.amp_spinbox.setSuffix(" V")
        control_layout.addWidget(self.amp_spinbox)
        
        control_layout.addWidget(QLabel("Samples:"))
        self.samples_spinbox = QSpinBox()
        self.samples_spinbox.setRange(100, 100000)
        self.samples_spinbox.setValue(1000)
        control_layout.addWidget(self.samples_spinbox)
        
        layout.addLayout(control_layout)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Status label
        self.status_label = QLabel("Ready to plot")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
    
    def _setup_plot(self):
        """Setup the matplotlib plot."""
        # Clear any existing plots
        self.figure.clear()
        
        # Create subplots using GridSpec
        gs = GridSpec(2, 2, figure=self.figure, hspace=0.3, wspace=0.3)
        
        # Main signal plot
        self.ax_main = self.figure.add_subplot(gs[0, :])
        self.ax_main.set_title("Signal Visualization", fontsize=14, fontweight='bold')
        self.ax_main.set_xlabel("Time (s)")
        self.ax_main.set_ylabel("Amplitude (V)")
        self.ax_main.grid(True, alpha=0.3)
        
        # Frequency domain plot
        self.ax_freq = self.figure.add_subplot(gs[1, 0])
        self.ax_freq.set_title("Frequency Domain", fontsize=12)
        self.ax_freq.set_xlabel("Frequency (Hz)")
        self.ax_freq.set_ylabel("Magnitude")
        self.ax_freq.grid(True, alpha=0.3)
        
        # Phase plot
        self.ax_phase = self.figure.add_subplot(gs[1, 1])
        self.ax_phase.set_title("Phase", fontsize=12)
        self.ax_phase.set_xlabel("Frequency (Hz)")
        self.ax_phase.set_ylabel("Phase (rad)")
        self.ax_phase.grid(True, alpha=0.3)
        
        # Initialize empty plots
        self.line_main, = self.ax_main.plot([], [], 'b-', linewidth=2, label='Signal')
        self.line_freq, = self.ax_freq.plot([], [], 'r-', linewidth=2, label='FFT')
        self.line_phase, = self.ax_phase.plot([], [], 'g-', linewidth=2, label='Phase')
        
        # Add legends
        self.ax_main.legend()
        self.ax_freq.legend()
        self.ax_phase.legend()
        
        # Draw the plot
        self.canvas.draw()
    
    def _connect_signals(self):
        """Connect widget signals."""
        self.plot_btn.clicked.connect(self.plot_signal)
        self.clear_btn.clicked.connect(self.clear_plot)
        self.grid_btn.toggled.connect(self.toggle_grid)
        
        # Parameter change connections
        self.freq_spinbox.valueChanged.connect(self.on_parameters_changed)
        self.amp_spinbox.valueChanged.connect(self.on_parameters_changed)
        self.samples_spinbox.valueChanged.connect(self.on_parameters_changed)
    
    def plot_signal(self):
        """Plot a mathematical signal."""
        try:
            # Get parameters
            frequency = self.freq_spinbox.value()
            amplitude = self.amp_spinbox.value()
            samples = self.samples_spinbox.value()
            sample_rate = 44100.0  # Standard audio sample rate
            
            # Generate time vector
            duration = samples / sample_rate
            t = np.linspace(0, duration, samples)
            
            # Generate sine wave signal
            signal = amplitude * np.sin(2 * np.pi * frequency * t)
            
            # Plot time domain
            self.line_main.set_data(t, signal)
            self.ax_main.set_xlim(0, duration)
            self.ax_main.set_ylim(-amplitude * 1.1, amplitude * 1.1)
            
            # Compute and plot FFT
            fft_result = np.fft.fft(signal)
            freqs = np.fft.fftfreq(samples, 1/sample_rate)
            
            # Only plot positive frequencies
            positive_freqs = freqs[:samples//2]
            positive_fft = np.abs(fft_result[:samples//2])
            
            self.line_freq.set_data(positive_freqs, positive_fft)
            self.ax_freq.set_xlim(0, sample_rate/2)
            self.ax_freq.set_ylim(0, np.max(positive_fft) * 1.1)
            
            # Plot phase
            phase = np.angle(fft_result[:samples//2])
            self.line_phase.set_data(positive_freqs, phase)
            self.ax_phase.set_xlim(0, sample_rate/2)
            self.ax_phase.set_ylim(-np.pi, np.pi)
            
            # Update plot
            self.canvas.draw()
            
            # Update status
            self.status_label.setText(f"Plotted: {frequency} Hz, {amplitude} V, {samples} samples")
            
            # Emit signal
            self.plot_updated.emit({
                'frequency': frequency,
                'amplitude': amplitude,
                'samples': samples,
                'signal': signal,
                'time': t,
                'fft': fft_result,
                'frequencies': freqs
            })
            
            logger.info(f"Signal plotted: {frequency} Hz, {amplitude} V")
            
        except Exception as e:
            logger.error(f"Error plotting signal: {e}")
            self.status_label.setText(f"Error: {str(e)}")
    
    def clear_plot(self):
        """Clear all plots."""
        # Clear data
        self.line_main.set_data([], [])
        self.line_freq.set_data([], [])
        self.line_phase.set_data([], [])
        
        # Reset axes
        self.ax_main.set_xlim(0, 1)
        self.ax_main.set_ylim(-1, 1)
        self.ax_freq.set_xlim(0, 1)
        self.ax_freq.set_ylim(0, 1)
        self.ax_phase.set_xlim(0, 1)
        self.ax_phase.set_ylim(-np.pi, np.pi)
        
        # Update plot
        self.canvas.draw()
        
        # Update status
        self.status_label.setText("Plot cleared")
        
        logger.info("Plot cleared")
    
    def toggle_grid(self, enabled):
        """Toggle grid display."""
        self.ax_main.grid(enabled, alpha=0.3)
        self.ax_freq.grid(enabled, alpha=0.3)
        self.ax_phase.grid(enabled, alpha=0.3)
        
        self.canvas.draw()
        
        status = "Grid enabled" if enabled else "Grid disabled"
        self.status_label.setText(status)
        logger.info(f"Grid {status}")
    
    def on_parameters_changed(self):
        """Handle parameter changes."""
        # Auto-plot when parameters change
        self.plot_signal()
    
    def plot_custom_signal(self, time_data, signal_data, title="Custom Signal"):
        """Plot custom signal data."""
        try:
            # Plot time domain
            self.line_main.set_data(time_data, signal_data)
            self.ax_main.set_xlim(np.min(time_data), np.max(time_data))
            self.ax_main.set_ylim(np.min(signal_data) * 1.1, np.max(signal_data) * 1.1)
            self.ax_main.set_title(title, fontsize=14, fontweight='bold')
            
            # Compute FFT if we have enough data
            if len(signal_data) > 1:
                fft_result = np.fft.fft(signal_data)
                dt = time_data[1] - time_data[0] if len(time_data) > 1 else 1.0
                freqs = np.fft.fftfreq(len(signal_data), dt)
                
                # Only plot positive frequencies
                positive_freqs = freqs[:len(signal_data)//2]
                positive_fft = np.abs(fft_result[:len(signal_data)//2])
                
                self.line_freq.set_data(positive_freqs, positive_fft)
                self.ax_freq.set_xlim(0, np.max(positive_freqs))
                self.ax_freq.set_ylim(0, np.max(positive_fft) * 1.1)
                
                # Plot phase
                phase = np.angle(fft_result[:len(signal_data)//2])
                self.line_phase.set_data(positive_freqs, phase)
                self.ax_phase.set_xlim(0, np.max(positive_freqs))
                self.ax_phase.set_ylim(-np.pi, np.pi)
            
            # Update plot
            self.canvas.draw()
            
            # Update status
            self.status_label.setText(f"Custom signal plotted: {len(signal_data)} points")
            
            logger.info(f"Custom signal plotted: {len(signal_data)} points")
            
        except Exception as e:
            logger.error(f"Error plotting custom signal: {e}")
            self.status_label.setText(f"Error: {str(e)}")
    
    def save_plot(self, filename):
        """Save the current plot to file."""
        try:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            self.status_label.setText(f"Plot saved: {filename}")
            logger.info(f"Plot saved: {filename}")
        except Exception as e:
            logger.error(f"Error saving plot: {e}")
            self.status_label.setText(f"Error saving: {str(e)}")


class RealTimePlot2DWidget(Plot2DWidget):
    """Real-time 2D plotting widget using pyqtgraph."""
    
    def __init__(self, parent=None):
        """Initialize real-time plot widget."""
        super().__init__(parent)
        self._setup_realtime_plot()
        logger.info("Real-time 2D Plot widget initialized")
    
    def _setup_realtime_plot(self):
        """Setup real-time plotting capabilities."""
        # This would integrate pyqtgraph for real-time plotting
        # For now, we'll use matplotlib with animation
        self.realtime_mode = False
        self.data_buffer = []
        self.max_buffer_size = 1000
    
    def start_realtime(self):
        """Start real-time plotting mode."""
        self.realtime_mode = True
        self.status_label.setText("Real-time mode started")
        logger.info("Real-time plotting started")
    
    def stop_realtime(self):
        """Stop real-time plotting mode."""
        self.realtime_mode = False
        self.status_label.setText("Real-time mode stopped")
        logger.info("Real-time plotting stopped")
    
    def add_realtime_data(self, data_point):
        """Add data point to real-time plot."""
        if not self.realtime_mode:
            return
        
        self.data_buffer.append(data_point)
        
        # Keep buffer size manageable
        if len(self.data_buffer) > self.max_buffer_size:
            self.data_buffer.pop(0)
        
        # Update plot
        if len(self.data_buffer) > 1:
            time_data = np.arange(len(self.data_buffer))
            self.plot_custom_signal(time_data, self.data_buffer, "Real-time Signal")

