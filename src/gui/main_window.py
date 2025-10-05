"""Main window for SignalAnalyzer desktop application."""

import sys
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QMenuBar, QStatusBar, QToolBar, QMenu,
    QLabel, QPushButton, QSplitter, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QKeySequence, QPixmap, QAction

from ..utils.logger import setup_logger
from ..gui.localization import tr

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window for SignalAnalyzer."""
    
    # Signals for communication between components
    signal_generated = pyqtSignal(dict)  # Emitted when signal is generated
    analysis_requested = pyqtSignal(dict)  # Emitted when analysis is requested
    visualization_changed = pyqtSignal(str)  # Emitted when visualization mode changes
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle(tr("SignalAnalyzer - Desktop Signal Analysis Tool"))
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Initialize components
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_status_bar()
        self._setup_central_widget()
        self._setup_connections()
        
        logger.info("Main window initialized successfully")
    
    def _setup_ui(self):
        """Setup the main UI components."""
        # Set window properties
        self.setWindowState(Qt.WindowState.WindowMaximized)
        
        # Set application icon (placeholder)
        # self.setWindowIcon(QIcon(":/icons/signal_analyzer.png"))
    
    def _setup_menu_bar(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        # New Signal
        new_action = QAction("&New Signal", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.setStatusTip("Create a new signal")
        new_action.triggered.connect(self.new_signal)
        file_menu.addAction(new_action)
        
        # Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.setStatusTip("Open existing signal file")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.setStatusTip("Save current signal")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        # Copy
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.setStatusTip("Copy selected data")
        edit_menu.addAction(copy_action)
        
        # Paste
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.setStatusTip("Paste data")
        edit_menu.addAction(paste_action)
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        
        # Toggle Fullscreen
        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.setStatusTip("Toggle fullscreen mode")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Analysis Menu
        analysis_menu = menubar.addMenu("&Analysis")
        
        # FFT Analysis
        fft_action = QAction("&FFT Analysis", self)
        fft_action.setStatusTip("Perform FFT analysis")
        fft_action.triggered.connect(self.fft_analysis)
        analysis_menu.addAction(fft_action)
        
        # Spectral Analysis
        spectral_action = QAction("&Spectral Analysis", self)
        spectral_action.setStatusTip("Perform spectral analysis")
        spectral_action.triggered.connect(self.spectral_analysis)
        analysis_menu.addAction(spectral_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        # About
        about_action = QAction("&About", self)
        about_action.setStatusTip("About SignalAnalyzer")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _setup_toolbar(self):
        """Setup the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        
        # New Signal
        new_action = QAction("New", self)
        new_action.setStatusTip("Create new signal")
        new_action.triggered.connect(self.new_signal)
        toolbar.addAction(new_action)
        
        # Generate Signal
        generate_action = QAction("Generate", self)
        generate_action.setStatusTip("Generate signal")
        generate_action.triggered.connect(self.generate_signal)
        toolbar.addAction(generate_action)
        
        toolbar.addSeparator()
        
        # Play/Pause
        play_action = QAction("Play", self)
        play_action.setStatusTip("Play/stop signal")
        play_action.triggered.connect(self.toggle_playback)
        toolbar.addAction(play_action)
        
        # Record
        record_action = QAction("Record", self)
        record_action.setStatusTip("Start/stop recording")
        record_action.triggered.connect(self.toggle_recording)
        toolbar.addAction(record_action)
        
        toolbar.addSeparator()
        
        # Zoom In
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setStatusTip("Zoom in")
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)
        
        # Zoom Out
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setStatusTip("Zoom out")
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)
    
    def _setup_status_bar(self):
        """Setup the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QLabel("")
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Show initial status
        self.status_bar.showMessage("SignalAnalyzer ready", 2000)
    
    def _setup_central_widget(self):
        """Setup the central widget with tabs."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel for signal configuration
       # self._create_left_panel(splitter)
        
        # Right panel for visualization tabs
        self._create_right_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 1100])
    
    def _create_left_panel(self, parent):
        """Create the left panel for signal configuration."""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Signal Configuration Group
        config_frame = QFrame()
        config_frame.setFrameStyle(QFrame.Shape.Box)
        config_layout = QVBoxLayout(config_frame)
        
        config_title = QLabel("Signal Configuration")
        config_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        config_layout.addWidget(config_title)
        
        # Frequency
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Frequency:"))
        self.freq_label = QLabel("1000 Hz")
        freq_layout.addWidget(self.freq_label)
        config_layout.addLayout(freq_layout)
        
        # Amplitude
        amp_layout = QHBoxLayout()
        amp_layout.addWidget(QLabel("Amplitude:"))
        self.amp_label = QLabel("1.0 V")
        amp_layout.addWidget(self.amp_label)
        config_layout.addLayout(amp_layout)
        
        # Law Type
        law_layout = QHBoxLayout()
        law_layout.addWidget(QLabel("Law Type:"))
        self.law_label = QLabel("Sine")
        law_layout.addWidget(self.law_label)
        config_layout.addLayout(law_layout)
        
        # Generate Button
        self.generate_btn = QPushButton("Generate Signal")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_signal)
        config_layout.addWidget(self.generate_btn)
        
        left_layout.addWidget(config_frame)
        
        # Analysis Controls Group
        analysis_frame = QFrame()
        analysis_frame.setFrameStyle(QFrame.Shape.Box)
        analysis_layout = QVBoxLayout(analysis_frame)
        
        analysis_title = QLabel("Analysis Controls")
        analysis_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        analysis_layout.addWidget(analysis_title)
        
        # FFT Button
        self.fft_btn = QPushButton("FFT Analysis")
        self.fft_btn.clicked.connect(self.fft_analysis)
        analysis_layout.addWidget(self.fft_btn)
        
        # Spectral Button
        self.spectral_btn = QPushButton("Spectral Analysis")
        self.spectral_btn.clicked.connect(self.spectral_analysis)
        analysis_layout.addWidget(self.spectral_btn)
        
        left_layout.addWidget(analysis_frame)
        
        # Add stretch to push everything to top
        left_layout.addStretch()
        
        parent.addWidget(left_widget)
    
    def _create_right_panel(self, parent):
        """Create the right panel with visualization tabs."""
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Signal Generator Tab
        self._create_signal_generator_tab()
        
        # 2D Plot Tab
        self._create_2d_plot_tab()
        
        # 3D Plot Tab
        self._create_3d_plot_tab()
        
        # Spectrum Tab
        self._create_spectrum_tab()
        
        # Oscilloscope Tab
        self._create_oscilloscope_tab()
        
        # Strobe Tab
        self._create_strobe_tab()
        
        parent.addWidget(self.tab_widget)
    
    def _create_signal_generator_tab(self):
        """Create the signal generator tab."""
        signal_widget = QWidget()
        signal_layout = QVBoxLayout(signal_widget)
        
        # Title
        title = QLabel("Signal Generator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        signal_layout.addWidget(title)
        
        # Placeholder content
        placeholder = QLabel("""
        <div style='text-align: center; color: #666; padding: 50px;'>
            <h3>Signal Generator</h3>
            <p>Configure signal parameters in the left panel</p>
            <p>Click 'Generate Signal' to create a mathematical signal</p>
            <p>Use the tabs above to visualize the signal</p>
        </div>
        """)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        signal_layout.addWidget(placeholder)
        
        # Add stretch
        signal_layout.addStretch()
        
        self.tab_widget.addTab(signal_widget, "Signal Generator")
    
    def _create_2d_plot_tab(self):
        """Create the 2D plot tab."""
        try:
            from ..visualization.matplotlib_2d import Plot2DWidget
            # Use the actual matplotlib widget
            self.plot_2d_widget = Plot2DWidget()
            self.tab_widget.addTab(self.plot_2d_widget, "2D Plot")
            
            # Connect signals
            self.plot_2d_widget.plot_updated.connect(self.on_plot_updated)
            
        except ImportError:
            # Fallback to placeholder if matplotlib not available
            plot_2d_widget = QWidget()
            plot_2d_layout = QVBoxLayout(plot_2d_widget)
            
            # Title
            title = QLabel("2D Plot Visualization")
            title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            plot_2d_layout.addWidget(title)
            
            # Placeholder for matplotlib plot
            plot_placeholder = QLabel("""
            <div style='text-align: center; color: #666; padding: 50px; border: 2px dashed #ccc; margin: 20px;'>
                <h3>2D Plot Area</h3>
                <p>Matplotlib integration will be displayed here</p>
                <p>Real-time signal visualization</p>
                <p>Interactive zoom and pan</p>
                <p style='color: #f44336;'>Note: matplotlib not available</p>
            </div>
            """)
            plot_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            plot_2d_layout.addWidget(plot_placeholder)
            
            # Add stretch
            plot_2d_layout.addStretch()
            
            self.tab_widget.addTab(plot_2d_widget, "2D Plot")
    
    def _create_3d_plot_tab(self):
        """Create the 3D plot tab."""
        plot_3d_widget = QWidget()
        plot_3d_layout = QVBoxLayout(plot_3d_widget)
        
        # Title
        title = QLabel("3D Plot Visualization")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plot_3d_layout.addWidget(title)
        
        # Placeholder for 3D plot
        plot_placeholder = QLabel("""
        <div style='text-align: center; color: #666; padding: 50px; border: 2px dashed #ccc; margin: 20px;'>
            <h3>3D Plot Area</h3>
            <p>PyOpenGL 3D visualization will be displayed here</p>
            <p>Interactive 3D surface plots</p>
            <p>GPU-accelerated rendering</p>
        </div>
        """)
        plot_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plot_3d_layout.addWidget(plot_placeholder)
        
        # Add stretch
        plot_3d_layout.addStretch()
        
        self.tab_widget.addTab(plot_3d_widget, "3D Plot")
    
    def _create_spectrum_tab(self):
        """Create the spectrum analysis tab."""
        spectrum_widget = QWidget()
        spectrum_layout = QVBoxLayout(spectrum_widget)
        
        # Title
        title = QLabel("Spectrum Analysis")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spectrum_layout.addWidget(title)
        
        # Placeholder for spectrum plot
        spectrum_placeholder = QLabel("""
        <div style='text-align: center; color: #666; padding: 50px; border: 2px dashed #ccc; margin: 20px;'>
            <h3>Spectrum Analysis Area</h3>
            <p>FFT and spectral analysis results will be displayed here</p>
            <p>Harmonic components visualization</p>
            <p>Frequency domain analysis</p>
        </div>
        """)
        spectrum_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spectrum_layout.addWidget(spectrum_placeholder)
        
        # Add stretch
        spectrum_layout.addStretch()
        
        self.tab_widget.addTab(spectrum_widget, "Spectrum")
    
    def _create_oscilloscope_tab(self):
        """Create the oscilloscope tab."""
        oscilloscope_widget = QWidget()
        oscilloscope_layout = QVBoxLayout(oscilloscope_widget)
        
        # Title
        title = QLabel("Real-time Oscilloscope")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        oscilloscope_layout.addWidget(title)
        
        # Placeholder for oscilloscope
        oscilloscope_placeholder = QLabel("""
        <div style='text-align: center; color: #666; padding: 50px; border: 2px dashed #ccc; margin: 20px;'>
            <h3>Oscilloscope Display</h3>
            <p>Real-time signal monitoring will be displayed here</p>
            <p>Multi-channel oscilloscope</p>
            <p>60+ FPS performance target</p>
        </div>
        """)
        oscilloscope_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        oscilloscope_layout.addWidget(oscilloscope_placeholder)
        
        # Add stretch
        oscilloscope_layout.addStretch()
        
        self.tab_widget.addTab(oscilloscope_widget, "Oscilloscope")
    
    def _create_strobe_tab(self):
        """Create the strobe tab."""
        try:
            from ..gui.strobe_widget import StrobeConfigWidget
            from ..visualization.strobe_plot import StrobePlotWidget
            
            # Create splitter for strobe config and visualization
            strobe_widget = QWidget()
            strobe_layout = QHBoxLayout(strobe_widget)
            
            # Left side - Strobe configuration
            self.strobe_config_widget = StrobeConfigWidget()
            strobe_layout.addWidget(self.strobe_config_widget, 1)
            
            # Right side - Strobe visualization
            self.strobe_plot_widget = StrobePlotWidget()
            strobe_layout.addWidget(self.strobe_plot_widget, 2)
            
            # Connect signals
            self.strobe_config_widget.strobe_generated.connect(self.strobe_plot_widget.plot_strobe)
            
            self.tab_widget.addTab(strobe_widget, "Стробы")
            
        except ImportError:
            # Fallback to placeholder if strobe modules not available
            strobe_widget = QWidget()
            strobe_layout = QVBoxLayout(strobe_widget)
            
            # Title
            title = QLabel("Система стробов")
            title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            strobe_layout.addWidget(title)
            
            # Placeholder
            strobe_placeholder = QLabel("""
            <div style='text-align: center; color: #666; padding: 50px; border: 2px dashed #ccc; margin: 20px;'>
                <h3>Система стробов и лучей</h3>
                <p>Конфигурация стробов будет здесь</p>
                <p>Визуализация лучей в реальном времени</p>
                <p>Генерация тестовых сигналов</p>
                <p style='color: #f44336;'>Примечание: модули стробов недоступны</p>
            </div>
            """)
            strobe_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            strobe_layout.addWidget(strobe_placeholder)
            
            strobe_layout.addStretch()
            
            self.tab_widget.addTab(strobe_widget, "Стробы")
    
    def _setup_connections(self):
        """Setup signal connections."""
        # Connect tab change signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Connect internal signals
        self.signal_generated.connect(self.on_signal_generated)
        self.analysis_requested.connect(self.on_analysis_requested)
    
    # Menu action handlers
    def new_signal(self):
        """Create a new signal."""
        self.status_bar.showMessage("Creating new signal...", 2000)
        logger.info("New signal requested")
        # TODO: Implement new signal creation
    
    def open_file(self):
        """Open an existing signal file."""
        self.status_bar.showMessage("Opening file...", 2000)
        logger.info("Open file requested")
        # TODO: Implement file opening
    
    def save_file(self):
        """Save current signal."""
        self.status_bar.showMessage("Saving file...", 2000)
        logger.info("Save file requested")
        # TODO: Implement file saving
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
            self.status_bar.showMessage("Exited fullscreen", 2000)
        else:
            self.showFullScreen()
            self.status_bar.showMessage("Entered fullscreen", 2000)
        logger.info("Fullscreen toggled")
    
    def fft_analysis(self):
        """Perform FFT analysis."""
        self.status_bar.showMessage("Performing FFT analysis...", 3000)
        logger.info("FFT analysis requested")
        # TODO: Implement FFT analysis
        self.analysis_requested.emit({"type": "fft"})
    
    def spectral_analysis(self):
        """Perform spectral analysis."""
        self.status_bar.showMessage("Performing spectral analysis...", 3000)
        logger.info("Spectral analysis requested")
        # TODO: Implement spectral analysis
        self.analysis_requested.emit({"type": "spectral"})
    
    def show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(self, "About SignalAnalyzer", 
                         "SignalAnalyzer v1.0.0\n\n"
                         "Desktop Signal Analysis Tool\n"
                         "Mathematical signal generation and visualization\n\n"
                         "Built with PyQt6, matplotlib, and PyOpenGL")
    
    # Toolbar action handlers
    def generate_signal(self):
        """Generate a new signal."""
        self.status_bar.showMessage("Generating signal...", 3000)
        logger.info("Signal generation requested")
        # TODO: Implement signal generation
        self.signal_generated.emit({
            "frequency": 1000.0,
            "amplitude": 1.0,
            "law_type": "sine"
        })
    
    def toggle_playback(self):
        """Toggle signal playback."""
        self.status_bar.showMessage("Toggling playback...", 2000)
        logger.info("Playback toggled")
        # TODO: Implement playback
    
    def toggle_recording(self):
        """Toggle signal recording."""
        self.status_bar.showMessage("Toggling recording...", 2000)
        logger.info("Recording toggled")
        # TODO: Implement recording
    
    def zoom_in(self):
        """Zoom in on plots."""
        self.status_bar.showMessage("Zooming in...", 1000)
        logger.info("Zoom in requested")
        # TODO: Implement zoom
    
    def zoom_out(self):
        """Zoom out on plots."""
        self.status_bar.showMessage("Zooming out...", 1000)
        logger.info("Zoom out requested")
        # TODO: Implement zoom
    
    # Signal handlers
    def on_tab_changed(self, index):
        """Handle tab change."""
        tab_name = self.tab_widget.tabText(index)
        self.status_bar.showMessage(f"Switched to {tab_name} tab", 2000)
        self.visualization_changed.emit(tab_name)
        logger.info(f"Tab changed to: {tab_name}")
    
    def on_signal_generated(self, signal_data):
        """Handle signal generation."""
        self.status_bar.showMessage("Signal generated successfully", 3000)
        logger.info(f"Signal generated: {signal_data}")
        # TODO: Update visualization
    
    def on_analysis_requested(self, analysis_data):
        """Handle analysis request."""
        self.status_bar.showMessage("Analysis completed", 3000)
        logger.info(f"Analysis requested: {analysis_data}")
        # TODO: Update analysis results
    
    def on_plot_updated(self, plot_data):
        """Handle plot update signal."""
        self.status_bar.showMessage("Plot updated", 2000)
        logger.info(f"Plot updated: {plot_data.get('frequency', 'unknown')} Hz")
        # TODO: Update other visualization tabs
    
    def closeEvent(self, event):
        """Handle window close event."""
        logger.info("Application closing")
        # TODO: Save settings and cleanup
        event.accept()


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("SignalAnalyzer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SignalAnalyzer")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logger.info("SignalAnalyzer GUI started")
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
