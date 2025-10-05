"""Database models for SignalAnalyzer application."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4, UUID
import numpy as np
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.dialects.sqlite import BLOB

Base = declarative_base()


class SignalData(Base):
    """Model for mathematical signal data with parameters, time series, and metadata."""
    
    __tablename__ = "signal_data"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Signal Parameters
    frequency = Column(Float, nullable=False)
    amplitude = Column(Float, nullable=False)
    phase = Column(Float, nullable=False, default=0.0)
    sample_rate = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    
    # Mathematical Law
    law_type = Column(String(50), nullable=False)
    law_parameters = Column(JSON, nullable=False)
    
    # Data (stored as binary)
    time_series = Column(BLOB, nullable=True)
    frequency_series = Column(BLOB, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    
    # Relationships
    analysis_sessions = relationship("AnalysisSession", secondary="analysis_signal_association", back_populates="signal_data")
    
    def __init__(self, **kwargs):
        """Initialize SignalData with validation."""
        super().__init__(**kwargs)
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate signal parameters."""
        if self.frequency <= 0:
            raise ValueError("Frequency must be positive")
        if self.amplitude <= 0:
            raise ValueError("Amplitude must be positive")
        if self.sample_rate <= 0:
            raise ValueError("Sample rate must be positive")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if self.law_type not in ['sine', 'cosine', 'square', 'triangle', 'custom']:
            raise ValueError("Invalid law type")
        if not isinstance(self.law_parameters, dict):
            raise TypeError("Law parameters must be a dictionary")
        if not isinstance(self.metadata, (dict, type(None))):
            raise TypeError("Metadata must be a dictionary")
        if not isinstance(self.tags, (list, type(None))):
            raise TypeError("Tags must be a list of strings")
        if self.tags is not None:
            if not all(isinstance(tag, str) for tag in self.tags):
                raise TypeError("Tags must be a list of strings")
    
    def set_time_series(self, time_series: np.ndarray):
        """Set time series data."""
        expected_length = int(self.sample_rate * self.duration)
        if len(time_series) != expected_length:
            raise ValueError(f"Time series length mismatch: expected {expected_length}, got {len(time_series)}")
        self.time_series = time_series.tobytes()
    
    def get_time_series(self) -> Optional[np.ndarray]:
        """Get time series data."""
        if self.time_series is None:
            return None
        return np.frombuffer(self.time_series, dtype=np.float64)
    
    def set_frequency_series(self, frequency_series: np.ndarray):
        """Set frequency series data."""
        self.frequency_series = frequency_series.tobytes()
    
    def get_frequency_series(self) -> Optional[np.ndarray]:
        """Get frequency series data."""
        if self.frequency_series is None:
            return None
        return np.frombuffer(self.frequency_series, dtype=np.complex128)
    
    def validate_law_parameters(self) -> bool:
        """Validate law parameters based on law type."""
        if self.law_type == 'sine':
            required_params = ['frequency', 'amplitude']
        elif self.law_type == 'cosine':
            required_params = ['frequency', 'amplitude']
        elif self.law_type == 'square':
            required_params = ['frequency', 'amplitude', 'duty_cycle']
        elif self.law_type == 'triangle':
            required_params = ['frequency', 'amplitude']
        elif self.law_type == 'custom':
            required_params = []
        else:
            return False
        
        return all(param in self.law_parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'frequency': self.frequency,
            'amplitude': self.amplitude,
            'phase': self.phase,
            'sample_rate': self.sample_rate,
            'duration': self.duration,
            'law_type': self.law_type,
            'law_parameters': self.law_parameters,
            'metadata': self.metadata,
            'tags': self.tags
        }


class AnalysisSession(Base):
    """Model for analysis workflow including input parameters, generated data, and visualization states."""
    
    __tablename__ = "analysis_sessions"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Session State
    status = Column(String(50), nullable=False, default="created")  # created, running, completed, failed
    progress = Column(Float, nullable=False, default=0.0)  # 0.0 to 1.0
    
    # Analysis Parameters
    analysis_type = Column(String(100), nullable=False)
    analysis_parameters = Column(JSON, nullable=False)
    
    # Visualization Settings
    visualization_settings = Column(JSON, nullable=True)
    
    # Results
    results = Column(JSON, nullable=True)
    
    # Relationships
    signal_data = relationship("SignalData", secondary="analysis_signal_association", back_populates="analysis_sessions")
    
    def __init__(self, **kwargs):
        """Initialize AnalysisSession with validation."""
        super().__init__(**kwargs)
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate analysis parameters."""
        if self.status not in ['created', 'running', 'completed', 'failed']:
            raise ValueError("Invalid status")
        if not 0.0 <= self.progress <= 1.0:
            raise ValueError("Progress must be between 0.0 and 1.0")
        if not isinstance(self.analysis_parameters, dict):
            raise TypeError("Analysis parameters must be a dictionary")
        if not isinstance(self.visualization_settings, (dict, type(None))):
            raise TypeError("Visualization settings must be a dictionary")
        if not isinstance(self.results, (dict, type(None))):
            raise TypeError("Results must be a dictionary")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'progress': self.progress,
            'analysis_type': self.analysis_type,
            'analysis_parameters': self.analysis_parameters,
            'visualization_settings': self.visualization_settings,
            'results': self.results
        }


class MathematicalLaw(Base):
    """Model for mathematical law definitions and parameters."""
    
    __tablename__ = "mathematical_laws"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Law Definition
    law_type = Column(String(50), nullable=False)
    parameters = Column(JSON, nullable=False)
    
    # Validation
    is_valid = Column(Boolean, nullable=False, default=True)
    validation_errors = Column(JSON, nullable=True)
    
    def __init__(self, **kwargs):
        """Initialize MathematicalLaw with validation."""
        super().__init__(**kwargs)
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate law parameters."""
        if self.law_type not in ['sine', 'cosine', 'square', 'triangle', 'custom']:
            raise ValueError("Invalid law type")
        if not isinstance(self.parameters, dict):
            raise TypeError("Parameters must be a dictionary")
        if not isinstance(self.validation_errors, (list, type(None))):
            raise TypeError("Validation errors must be a list")
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters against law definition."""
        if self.law_type == 'sine':
            required_params = ['frequency', 'amplitude']
        elif self.law_type == 'cosine':
            required_params = ['frequency', 'amplitude']
        elif self.law_type == 'square':
            required_params = ['frequency', 'amplitude', 'duty_cycle']
        elif self.law_type == 'triangle':
            required_params = ['frequency', 'amplitude']
        elif self.law_type == 'custom':
            required_params = []
        else:
            return False
        
        return all(param in parameters for param in required_params)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'law_type': self.law_type,
            'parameters': self.parameters,
            'is_valid': self.is_valid,
            'validation_errors': self.validation_errors
        }


class SpectralAnalysis(Base):
    """Model for spectral analysis results."""
    
    __tablename__ = "spectral_analyses"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Analysis Parameters
    analysis_type = Column(String(100), nullable=False)  # fft, stft, psd, harmonic
    window_size = Column(Integer, nullable=True)
    hop_size = Column(Integer, nullable=True)
    window_function = Column(String(50), nullable=True)
    
    # Results
    frequencies = Column(BLOB, nullable=True)
    magnitudes = Column(BLOB, nullable=True)
    phases = Column(BLOB, nullable=True)
    
    # Metadata
    sample_rate = Column(Float, nullable=False)
    analysis_parameters = Column(JSON, nullable=True)
    
    # Relationships
    signal_data_id = Column(PostgresUUID(as_uuid=True), ForeignKey('signal_data.id'), nullable=False)
    signal_data = relationship("SignalData")
    
    def __init__(self, **kwargs):
        """Initialize SpectralAnalysis with validation."""
        super().__init__(**kwargs)
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate analysis parameters."""
        if self.analysis_type not in ['fft', 'stft', 'psd', 'harmonic']:
            raise ValueError("Invalid analysis type")
        if self.sample_rate <= 0:
            raise ValueError("Sample rate must be positive")
        if not isinstance(self.analysis_parameters, (dict, type(None))):
            raise TypeError("Analysis parameters must be a dictionary")
    
    def set_frequencies(self, frequencies: np.ndarray):
        """Set frequency data."""
        self.frequencies = frequencies.tobytes()
    
    def get_frequencies(self) -> Optional[np.ndarray]:
        """Get frequency data."""
        if self.frequencies is None:
            return None
        return np.frombuffer(self.frequencies, dtype=np.float64)
    
    def set_magnitudes(self, magnitudes: np.ndarray):
        """Set magnitude data."""
        self.magnitudes = magnitudes.tobytes()
    
    def get_magnitudes(self) -> Optional[np.ndarray]:
        """Get magnitude data."""
        if self.magnitudes is None:
            return None
        return np.frombuffer(self.magnitudes, dtype=np.float64)
    
    def set_phases(self, phases: np.ndarray):
        """Set phase data."""
        self.phases = phases.tobytes()
    
    def get_phases(self) -> Optional[np.ndarray]:
        """Get phase data."""
        if self.phases is None:
            return None
        return np.frombuffer(self.phases, dtype=np.float64)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'analysis_type': self.analysis_type,
            'window_size': self.window_size,
            'hop_size': self.hop_size,
            'window_function': self.window_function,
            'sample_rate': self.sample_rate,
            'analysis_parameters': self.analysis_parameters,
            'signal_data_id': str(self.signal_data_id)
        }


class DatabaseConnection(Base):
    """Model for database connection configuration."""
    
    __tablename__ = "database_connections"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Basic information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Connection Configuration
    database_type = Column(String(50), nullable=False)  # sqlite, postgresql
    connection_string = Column(Text, nullable=False)
    connection_parameters = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    last_connected = Column(DateTime, nullable=True)
    connection_errors = Column(JSON, nullable=True)
    
    def __init__(self, **kwargs):
        """Initialize DatabaseConnection with validation."""
        super().__init__(**kwargs)
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Validate connection parameters."""
        if self.database_type not in ['sqlite', 'postgresql']:
            raise ValueError("Invalid database type")
        if not isinstance(self.connection_parameters, (dict, type(None))):
            raise TypeError("Connection parameters must be a dictionary")
        if not isinstance(self.connection_errors, (list, type(None))):
            raise TypeError("Connection errors must be a list")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'database_type': self.database_type,
            'connection_string': self.connection_string,
            'connection_parameters': self.connection_parameters,
            'is_active': self.is_active,
            'last_connected': self.last_connected.isoformat() if self.last_connected else None,
            'connection_errors': self.connection_errors
        }


# Association table for many-to-many relationship between AnalysisSession and SignalData
class AnalysisSignalAssociation(Base):
    """Association table for analysis sessions and signal data."""
    
    __tablename__ = "analysis_signal_association"
    
    analysis_session_id = Column(PostgresUUID(as_uuid=True), ForeignKey('analysis_sessions.id'), primary_key=True)
    signal_data_id = Column(PostgresUUID(as_uuid=True), ForeignKey('signal_data.id'), primary_key=True)
    
    # Additional metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    order_index = Column(Integer, nullable=False, default=0)
