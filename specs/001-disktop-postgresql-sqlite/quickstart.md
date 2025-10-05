# Quickstart Guide: Desktop Signal Analyzer

**Date**: 2025-10-04  
**Feature**: Desktop Signal Analyzer with Database Integration

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+ or Ubuntu 20.04+
- **Python**: 3.12 or higher
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Graphics**: OpenGL 3.3+ compatible GPU (NVIDIA/AMD/Intel)
- **Storage**: 2GB free space

### GPU Requirements (Optional but Recommended)
- **NVIDIA GPU**: CUDA 11.0+ for maximum performance
- **AMD/Intel GPU**: OpenGL 3.3+ for hardware acceleration
- **Fallback**: CPU-only mode available

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-org/signal-analyzer.git
cd signal-analyzer
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Ubuntu
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# Install GPU acceleration (optional)
pip install cupy-cuda12x  # For NVIDIA GPUs with CUDA 12.x
```

### 4. Verify Installation
```bash
python -c "import PyQt6, numpy, scipy, matplotlib, pyqtgraph; print('All dependencies installed successfully')"
```

## First Run

### 1. Launch Application
```bash
python main.py
```

### 2. Initial Configuration
1. **Database Setup**: Choose SQLite (default) or PostgreSQL
2. **GPU Detection**: Application will automatically detect available GPU
3. **Directory Setup**: Application creates required data directories

### 3. Create First Signal
1. **Signal Generator**: Click "New Signal" button
2. **Configure Parameters**:
   - Frequency: 1000 Hz
   - Amplitude: 1.0 V
   - Duration: 1.0 s
   - Sample Rate: 44100 Hz
3. **Generate Signal**: Click "Generate" button
4. **View Results**: Signal appears in 2D plot window

## Basic Workflow

### 1. Signal Generation
```python
# Example: Generate sine wave
signal_config = {
    "name": "Test Sine Wave",
    "frequency": 1000.0,
    "amplitude": 1.0,
    "phase": 0.0,
    "sample_rate": 44100.0,
    "duration": 1.0,
    "law_type": "sine"
}

# Generate signal
signal = generate_signal(signal_config)
```

### 2. Spectral Analysis
```python
# Perform FFT analysis
analysis_config = {
    "window_type": "hann",
    "window_size": 1024,
    "overlap": 0.5,
    "fft_size": 2048
}

# Analyze signal
spectrum = analyze_spectrum(signal, analysis_config)
```

### 3. 3D Visualization
```python
# Create 3D surface plot
surface_config = {
    "plot_type": "surface",
    "colormap": "viridis",
    "elevation": 30,
    "azimuth": 45
}

# Generate 3D plot
plot_3d(signal, surface_config)
```

## Configuration

### 1. JSON Configuration Files
Configuration files are stored in `config/` directory:

```bash
config/
├── signal_generators/     # Signal generation templates
├── analysis_methods/      # Analysis algorithm configurations
├── visualization/         # Plot and display settings
├── database/             # Database connection settings
└── gpu/                  # GPU acceleration settings
```

### 2. Example Configuration
```json
{
  "application": {
    "name": "Signal Analyzer",
    "version": "1.0.0",
    "theme": "dark"
  },
  "performance": {
    "gpu_acceleration": true,
    "max_memory_usage": "8GB",
    "real_time_fps": 60
  },
  "database": {
    "type": "sqlite",
    "file_path": "data/signals.db"
  }
}
```

## Data Management

### 1. Directory Structure
```
data/
├── input_data/           # Input signal files
├── output_data/          # Generated analysis results
└── validation/           # Validation reports
```

### 2. Import/Export
- **Import**: CSV, WAV, MAT files
- **Export**: CSV, JSON, PNG, PDF
- **Database**: PostgreSQL or SQLite

### 3. Data Validation
```python
# Validate signal quality
validation_report = validate_signal(signal)

# Check analysis accuracy
accuracy_report = validate_analysis(spectrum)

# Performance benchmarking
performance_report = benchmark_performance()
```

## Advanced Features

### 1. GPU Acceleration
```python
# Enable CUDA acceleration
import cupy as cp

# Transfer data to GPU
gpu_signal = cp.asarray(signal)

# Perform GPU computation
gpu_result = cp.fft.fft(gpu_signal)

# Transfer back to CPU
result = cp.asnarray(gpu_result)
```

### 2. Real-time Oscilloscope
```python
# Configure oscilloscope
oscilloscope_config = {
    "channels": 4,
    "sample_rate": 1000000,
    "buffer_size": 10000,
    "trigger": {
        "type": "edge",
        "level": 0.5,
        "slope": "rising"
    }
}

# Start real-time acquisition
start_oscilloscope(oscilloscope_config)
```

### 3. Spectral Analysis
```python
# Advanced spectral analysis
spectral_config = {
    "method": "welch",
    "window": "hann",
    "nperseg": 1024,
    "noverlap": 512,
    "nfft": 2048
}

# Perform analysis
psd = welch_psd(signal, **spectral_config)
```

## Troubleshooting

### Common Issues

#### 1. GPU Not Detected
```bash
# Check GPU availability
python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"

# Fallback to CPU
export CUDA_VISIBLE_DEVICES=""
```

#### 2. Database Connection Error
```bash
# Check database file permissions
ls -la data/signals.db

# Reset database
rm data/signals.db
python -c "from src.database import init_database; init_database()"
```

#### 3. Performance Issues
```bash
# Monitor GPU usage
nvidia-smi

# Check memory usage
python -c "import psutil; print(psutil.virtual_memory())"
```

### Performance Optimization

#### 1. GPU Memory Management
```python
# Clear GPU cache
import cupy as cp
cp.get_default_memory_pool().free_all_blocks()
```

#### 2. Data Chunking
```python
# Process large datasets in chunks
def process_large_signal(signal, chunk_size=10000):
    for i in range(0, len(signal), chunk_size):
        chunk = signal[i:i+chunk_size]
        yield process_chunk(chunk)
```

#### 3. Memory Optimization
```python
# Use memory-efficient data types
signal = signal.astype(np.float32)  # Use 32-bit instead of 64-bit
```

## Getting Help

### 1. Documentation
- **User Manual**: `docs/user_manual.md`
- **API Reference**: `docs/api_reference.md`
- **Examples**: `examples/` directory

### 2. Community Support
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas
- **Wiki**: Community-contributed documentation

### 3. Professional Support
- **Email**: support@signal-analyzer.com
- **Slack**: #signal-analyzer channel
- **Training**: Available for enterprise users

## Next Steps

1. **Explore Examples**: Check `examples/` directory for sample code
2. **Read Documentation**: Browse `docs/` for detailed information
3. **Join Community**: Participate in discussions and contribute
4. **Advanced Features**: Explore GPU acceleration and real-time analysis

Welcome to Desktop Signal Analyzer! 🚀
