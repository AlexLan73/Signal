#!/usr/bin/env python3
"""Full integration test for SignalAnalyzer GUI + Mathematical Engine."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
    from PyQt6.QtCore import Qt
    
    from src.visualization.matplotlib_2d import Plot2DWidget
    from src.math.signal_generator import SignalGenerator, SignalParameters, SignalType
    
    print("✅ All components imported successfully")
    
    class IntegrationTestWindow(QMainWindow):
        """Test window for GUI + Math integration."""
        
        def __init__(self):
            super().__init__()
            self.setWindowTitle("SignalAnalyzer - Integration Test")
            self.setGeometry(100, 100, 1200, 800)
            
            # Initialize components
            self.signal_generator = SignalGenerator()
            self.plot_widget = Plot2DWidget()
            
            self._setup_ui()
            self._test_integration()
        
        def _setup_ui(self):
            """Setup the test UI."""
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QVBoxLayout(central_widget)
            
            # Title
            title = QLabel("""
            <div style='text-align: center; padding: 20px;'>
                <h1>🎉 SignalAnalyzer Integration Test</h1>
                <h2>GUI + Mathematical Engine + Visualization</h2>
            </div>
            """)
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title)
            
            # Status
            self.status_label = QLabel("Ready for testing...")
            self.status_label.setStyleSheet("""
                padding: 10px;
                background-color: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 5px;
                font-weight: bold;
            """)
            layout.addWidget(self.status_label)
            
            # Test buttons
            test_layout = QVBoxLayout()
            
            self.test_sine_btn = QPushButton("Test Sine Wave")
            self.test_sine_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            self.test_sine_btn.clicked.connect(self.test_sine_wave)
            test_layout.addWidget(self.test_sine_btn)
            
            self.test_complex_btn = QPushButton("Test Complex Signal")
            self.test_complex_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)
            self.test_complex_btn.clicked.connect(self.test_complex_signal)
            test_layout.addWidget(self.test_complex_btn)
            
            self.test_square_btn = QPushButton("Test Square Wave")
            self.test_square_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9C27B0;
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7B1FA2;
                }
            """)
            self.test_square_btn.clicked.connect(self.test_square_wave)
            test_layout.addWidget(self.test_square_btn)
            
            layout.addLayout(test_layout)
            
            # Add the plot widget
            layout.addWidget(self.plot_widget)
        
        def _test_integration(self):
            """Test the integration between components."""
            self.status_label.setText("✅ Integration test ready - Click buttons to test signals")
        
        def test_sine_wave(self):
            """Test sine wave generation and plotting."""
            try:
                # Generate sine wave
                params = SignalParameters(
                    signal_type=SignalType.SINE,
                    frequency=1000.0,
                    amplitude=1.0,
                    duration=0.1
                )
                
                time, signal = self.signal_generator.generate_signal(params)
                
                # Plot the signal
                self.plot_widget.plot_custom_signal(time, signal, "Sine Wave Test")
                
                self.status_label.setText(f"✅ Sine wave: {params.frequency} Hz, {params.amplitude} V, {len(signal)} samples")
                
                # Get signal info
                info = self.signal_generator.get_signal_info()
                print(f"Signal info: {info}")
                
            except Exception as e:
                self.status_label.setText(f"❌ Error: {str(e)}")
                print(f"Error testing sine wave: {e}")
        
        def test_complex_signal(self):
            """Test complex signal generation and plotting."""
            try:
                # Generate complex signal
                params = SignalParameters(
                    signal_type=SignalType.COMPLEX,
                    frequency=440.0,
                    amplitude=1.0,
                    duration=0.1
                )
                
                time, signal = self.signal_generator.generate_signal(params)
                
                # Plot the signal
                self.plot_widget.plot_custom_signal(time, signal, "Complex Signal Test")
                
                self.status_label.setText(f"✅ Complex signal: {params.frequency} Hz, {params.amplitude} V, {len(signal)} samples")
                
                # Get signal info
                info = self.signal_generator.get_signal_info()
                print(f"Signal info: {info}")
                
            except Exception as e:
                self.status_label.setText(f"❌ Error: {str(e)}")
                print(f"Error testing complex signal: {e}")
        
        def test_square_wave(self):
            """Test square wave generation and plotting."""
            try:
                # Generate square wave
                params = SignalParameters(
                    signal_type=SignalType.SQUARE,
                    frequency=500.0,
                    amplitude=0.8,
                    duration=0.1,
                    duty_cycle=0.3
                )
                
                time, signal = self.signal_generator.generate_signal(params)
                
                # Plot the signal
                self.plot_widget.plot_custom_signal(time, signal, "Square Wave Test")
                
                self.status_label.setText(f"✅ Square wave: {params.frequency} Hz, {params.amplitude} V, duty={params.duty_cycle}")
                
                # Get signal info
                info = self.signal_generator.get_signal_info()
                print(f"Signal info: {info}")
                
            except Exception as e:
                self.status_label.setText(f"❌ Error: {str(e)}")
                print(f"Error testing square wave: {e}")
    
    # Create and show the test window
    app = QApplication(sys.argv)
    window = IntegrationTestWindow()
    window.show()
    
    print("✅ Integration test window created")
    print("\n🎯 What you can test:")
    print("  • Sine wave generation and plotting")
    print("  • Complex signal with harmonics")
    print("  • Square wave with custom duty cycle")
    print("  • Real-time FFT analysis")
    print("  • Interactive matplotlib plots")
    print("  • Signal statistics and information")
    
    print("\n🚀 Integration test ready!")
    print("Click the buttons to test different signal types")
    
    # Run the application
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"❌ Error importing components: {e}")
    print("Make sure all dependencies are installed:")
    print("  py -m pip install PyQt6 matplotlib numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Integration test failed: {e}")
    sys.exit(1)
