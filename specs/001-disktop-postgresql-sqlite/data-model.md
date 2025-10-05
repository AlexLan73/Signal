# Data Model: Desktop Signal Analyzer

**Date**: 2025-10-04  
**Feature**: Desktop Signal Analyzer with Database Integration

## Core Entities

### SignalData
Represents mathematical signal data with parameters, time series, and metadata.

```python
class SignalData:
    id: UUID                    # Unique identifier
    name: str                   # Human-readable name
    description: str            # Optional description
    created_at: datetime        # Creation timestamp
    updated_at: datetime        # Last modification timestamp
    
    # Signal Parameters
    frequency: float            # Base frequency (Hz)
    amplitude: float            # Signal amplitude
    phase: float               # Phase offset (radians)
    sample_rate: float         # Sampling rate (Hz)
    duration: float            # Signal duration (seconds)
    
    # Mathematical Law
    law_type: str              # 'sine', 'cosine', 'square', 'triangle', 'custom'
    law_parameters: dict       # JSON parameters for mathematical law
    
    # Data
    time_series: np.ndarray    # Time domain data
    frequency_series: np.ndarray # Frequency domain data (optional)
    
    # Metadata
    metadata: dict             # Additional signal properties
    tags: List[str]            # Searchable tags
```

### AnalysisSession
Represents a complete analysis workflow including input parameters, generated data, and visualization states.

```python
class AnalysisSession:
    id: UUID                   # Unique identifier
    name: str                  # Session name
    description: str           # Optional description
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last modification timestamp
    
    # Session State
    status: str                # 'active', 'paused', 'completed', 'archived'
    
    # Input Parameters
    input_signals: List[UUID]  # References to SignalData
    analysis_parameters: dict  # JSON analysis configuration
    
    # Results
    results: dict              # JSON analysis results
    visualizations: dict       # JSON visualization state
    
    # Database Connection
    database_config: dict      # Database connection parameters
    database_status: str       # 'connected', 'disconnected', 'error'
```

### MathematicalLaw
Represents configurable mathematical functions used for signal generation.

```python
class MathematicalLaw:
    id: UUID                   # Unique identifier
    name: str                  # Law name
    type: str                  # 'trigonometric', 'polynomial', 'exponential', 'custom'
    
    # Mathematical Definition
    formula: str               # Mathematical expression (SymPy compatible)
    parameters: dict           # JSON parameter definitions
    constraints: dict          # Parameter constraints and validation rules
    
    # Implementation
    python_code: str           # Python implementation
    gpu_code: str              # CUDA/OpenCL implementation (optional)
    
    # Metadata
    description: str           # Human-readable description
    category: str              # Law category
    tags: List[str]            # Searchable tags
```

### SpectralAnalysis
Represents frequency domain analysis results including harmonic components and envelope data.

```python
class SpectralAnalysis:
    id: UUID                   # Unique identifier
    signal_id: UUID            # Reference to SignalData
    session_id: UUID           # Reference to AnalysisSession
    created_at: datetime       # Creation timestamp
    
    # Analysis Parameters
    window_type: str           # 'hann', 'hamming', 'blackman', 'rectangular'
    window_size: int           # Window size in samples
    overlap: float             # Window overlap ratio
    fft_size: int              # FFT size
    
    # Results
    frequency_axis: np.ndarray # Frequency bins
    magnitude_spectrum: np.ndarray # Magnitude spectrum
    phase_spectrum: np.ndarray # Phase spectrum
    power_spectral_density: np.ndarray # PSD
    
    # Harmonic Analysis
    fundamental_frequency: float # Detected fundamental frequency
    harmonics: List[dict]      # Harmonic components with frequencies and amplitudes
    total_harmonic_distortion: float # THD percentage
    
    # Envelope Analysis
    envelope: np.ndarray       # Signal envelope
    envelope_spectrum: np.ndarray # Envelope frequency spectrum
    
    # Metadata
    analysis_metadata: dict    # Additional analysis parameters and results
```

### DatabaseConnection
Represents connection configuration and state for data persistence.

```python
class DatabaseConnection:
    id: UUID                   # Unique identifier
    name: str                  # Connection name
    type: str                  # 'postgresql', 'sqlite'
    
    # Connection Parameters
    host: str                  # Database host (PostgreSQL only)
    port: int                  # Database port (PostgreSQL only)
    database: str              # Database name
    username: str              # Username (PostgreSQL only)
    password: str              # Password (encrypted)
    
    # SQLite Specific
    file_path: str             # SQLite file path
    
    # Connection State
    status: str                # 'connected', 'disconnected', 'error'
    last_connected: datetime   # Last successful connection
    connection_pool_size: int  # Connection pool size
    
    # Configuration
    ssl_mode: str              # SSL mode (PostgreSQL only)
    timeout: int               # Connection timeout
    retry_attempts: int        # Retry attempts on failure
```

### ConfigurationFile
Represents JSON configuration files with example configurations.

```python
class ConfigurationFile:
    id: UUID                   # Unique identifier
    name: str                  # Configuration name
    file_path: str             # Relative path in config/ directory
    category: str              # Configuration category
    
    # Content
    content: dict              # JSON configuration content
    schema: dict               # JSON schema for validation
    version: str               # Configuration version
    
    # Metadata
    description: str           # Human-readable description
    is_example: bool           # Is this an example configuration
    tags: List[str]            # Searchable tags
    
    # Usage
    usage_count: int           # How many times used
    last_used: datetime        # Last usage timestamp
```

### ValidationReport
Represents validation results and analysis reports.

```python
class ValidationReport:
    id: UUID                   # Unique identifier
    name: str                  # Report name
    created_at: datetime       # Creation timestamp
    
    # Validation Context
    validation_type: str       # 'signal_quality', 'analysis_accuracy', 'performance'
    target_id: UUID            # ID of validated object
    target_type: str           # Type of validated object
    
    # Results
    status: str                # 'passed', 'failed', 'warning'
    score: float               # Validation score (0-100)
    issues: List[dict]         # List of validation issues
    
    # Metrics
    metrics: dict              # Validation metrics
    recommendations: List[str] # Improvement recommendations
    
    # Report
    report_content: str        # Human-readable report
    report_data: dict          # Structured report data
    
    # Storage
    file_path: str             # Path in validation/ directory
    file_size: int             # Report file size
```

## Database Schema

### PostgreSQL Tables

```sql
-- Signals table
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Signal parameters
    frequency DOUBLE PRECISION NOT NULL,
    amplitude DOUBLE PRECISION NOT NULL,
    phase DOUBLE PRECISION NOT NULL,
    sample_rate DOUBLE PRECISION NOT NULL,
    duration DOUBLE PRECISION NOT NULL,
    
    -- Mathematical law
    law_type VARCHAR(50) NOT NULL,
    law_parameters JSONB,
    
    -- Data (stored as binary or JSON)
    time_series BYTEA,
    frequency_series BYTEA,
    
    -- Metadata
    metadata JSONB,
    tags TEXT[]
);

-- Analysis sessions table
CREATE TABLE analysis_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Session state
    status VARCHAR(20) DEFAULT 'active',
    
    -- Parameters and results
    input_signals UUID[],
    analysis_parameters JSONB,
    results JSONB,
    visualizations JSONB,
    
    -- Database connection
    database_config JSONB,
    database_status VARCHAR(20) DEFAULT 'disconnected'
);

-- Spectral analysis table
CREATE TABLE spectral_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    signal_id UUID REFERENCES signals(id),
    session_id UUID REFERENCES analysis_sessions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Analysis parameters
    window_type VARCHAR(20),
    window_size INTEGER,
    overlap DOUBLE PRECISION,
    fft_size INTEGER,
    
    -- Results (stored as binary)
    frequency_axis BYTEA,
    magnitude_spectrum BYTEA,
    phase_spectrum BYTEA,
    power_spectral_density BYTEA,
    
    -- Harmonic analysis
    fundamental_frequency DOUBLE PRECISION,
    harmonics JSONB,
    total_harmonic_distortion DOUBLE PRECISION,
    
    -- Envelope analysis
    envelope BYTEA,
    envelope_spectrum BYTEA,
    
    -- Metadata
    analysis_metadata JSONB
);
```

### SQLite Tables

```sql
-- Signals table
CREATE TABLE signals (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    -- Signal parameters
    frequency REAL NOT NULL,
    amplitude REAL NOT NULL,
    phase REAL NOT NULL,
    sample_rate REAL NOT NULL,
    duration REAL NOT NULL,
    
    -- Mathematical law
    law_type TEXT NOT NULL,
    law_parameters TEXT, -- JSON
    
    -- Data (stored as BLOB)
    time_series BLOB,
    frequency_series BLOB,
    
    -- Metadata
    metadata TEXT, -- JSON
    tags TEXT -- JSON array
);

-- Analysis sessions table
CREATE TABLE analysis_sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    -- Session state
    status TEXT DEFAULT 'active',
    
    -- Parameters and results
    input_signals TEXT, -- JSON array
    analysis_parameters TEXT, -- JSON
    results TEXT, -- JSON
    visualizations TEXT, -- JSON
    
    -- Database connection
    database_config TEXT, -- JSON
    database_status TEXT DEFAULT 'disconnected'
);
```

## Data Directory Structure

```
data/
├── input_data/               # Input signal data
│   ├── raw_signals/         # Raw signal files
│   ├── imported_data/       # Imported data files
│   └── reference_signals/   # Reference signal library
├── output_data/             # Generated analysis results
│   ├── processed_signals/   # Processed signal data
│   ├── analysis_results/    # Analysis output files
│   ├── exported_data/       # Exported data files
│   └── reports/             # Generated reports
└── validation/              # Validation reports and logs
    ├── signal_validation/   # Signal quality validation
    ├── analysis_validation/ # Analysis accuracy validation
    ├── performance_logs/    # Performance validation logs
    └── error_reports/       # Error and exception reports
```

## JSON Configuration Examples

### Signal Generation Configuration
```json
{
  "signal_generation": {
    "name": "Sine Wave Generator",
    "type": "trigonometric",
    "parameters": {
      "frequency": 1000.0,
      "amplitude": 1.0,
      "phase": 0.0,
      "sample_rate": 44100.0,
      "duration": 1.0
    },
    "law": {
      "type": "sine",
      "formula": "A * sin(2 * pi * f * t + phi)",
      "variables": {
        "A": "amplitude",
        "f": "frequency", 
        "phi": "phase"
      }
    }
  }
}
```

### Analysis Configuration
```json
{
  "spectral_analysis": {
    "window": {
      "type": "hann",
      "size": 1024,
      "overlap": 0.5
    },
    "fft": {
      "size": 2048,
      "zero_padding": true
    },
    "harmonics": {
      "detection_threshold": 0.01,
      "max_harmonics": 10
    },
    "envelope": {
      "method": "hilbert",
      "smooth_factor": 0.1
    }
  }
}
```

### Database Configuration
```json
{
  "database": {
    "type": "sqlite",
    "connection": {
      "file_path": "data/signal_analyzer.db",
      "timeout": 30,
      "retry_attempts": 3
    },
    "pool": {
      "size": 5,
      "max_overflow": 10
    }
  }
}
```

This data model provides a comprehensive foundation for the Desktop Signal Analyzer application with support for mathematical signal generation, spectral analysis, database persistence, and validation reporting.
