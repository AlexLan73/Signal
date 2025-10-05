# Claude Code Instructions: Desktop Signal Analyzer

**Date**: 2025-10-04  
**Feature**: Desktop Signal Analyzer with Database Integration  
**AI Agent**: Claude Code

## Project Overview

You are working on a Desktop Signal Analyzer application built with Python and PyQt6. This is a cross-platform desktop application for mathematical signal analysis with real-time visualization, GPU acceleration, and database persistence.

## Architecture Guidelines

### 1. Layer Structure
```
GUI Layer (PyQt6) → Visualization Layer (pyqtgraph/PyOpenGL) → Data Processing Layer (NumPy/SciPy) → Storage Layer (SQLAlchemy)
```

### 2. Design Patterns
- **Observer Pattern**: Real-time data updates across components
- **Factory Pattern**: Database connection creation
- **Strategy Pattern**: GPU vs CPU computation selection
- **Command Pattern**: User action handling
- **Model-View-Controller**: Separation of concerns

### 3. Module Organization
```
src/
├── gui/                 # PyQt6 user interface
├── visualization/       # Plotting and 3D visualization
├── data/               # Data processing and analysis
├── math/               # Mathematical functions and signal generation
├── database/           # Database operations and models
├── config/             # Configuration management
└── utils/              # Utility functions and helpers
```

## Coding Standards

### 1. Python Style
- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use meaningful variable and function names

### 2. PyQt6 Guidelines
- Use QWidget subclasses for custom widgets
- Implement proper event handling
- Use QThread for long-running operations
- Follow Qt's memory management patterns

### 3. Performance Requirements
- GUI operations must complete within 16ms (60 FPS)
- Signal generation must achieve sub-millisecond response times
- Memory usage must remain stable during extended operation
- Use GPU acceleration when available

## Implementation Priorities

### 1. Core Functionality (Phase 1)
- **Signal Generation**: Mathematical signal creation with configurable parameters
- **Basic Visualization**: 2D plotting with matplotlib/pyqtgraph
- **Database Integration**: SQLite support with SQLAlchemy
- **Configuration Management**: JSON configuration files

### 2. Advanced Features (Phase 2)
- **3D Visualization**: PyOpenGL integration for 3D surfaces
- **Spectral Analysis**: FFT and harmonic analysis
- **Real-time Oscilloscope**: Multi-channel real-time display
- **GPU Acceleration**: CUDA integration for mathematical computations

### 3. Optimization (Phase 3)
- **Performance Tuning**: Memory optimization and caching
- **Cross-platform Testing**: Windows and Ubuntu compatibility
- **User Experience**: Smooth animations and responsive interface
- **Documentation**: Comprehensive user and developer documentation

## Testing Requirements

### 1. Unit Tests
- Test all mathematical functions with known test vectors
- Validate GUI component behavior
- Test database operations with mock data
- Verify configuration file parsing

### 2. Integration Tests
- End-to-end signal generation and visualization
- Database persistence and retrieval
- Cross-module communication
- Error handling and recovery

### 3. Performance Tests
- Measure signal generation speed
- Test GUI responsiveness under load
- Validate memory usage patterns
- Benchmark GPU acceleration benefits

## Error Handling

### 1. Graceful Degradation
- Fallback to CPU when GPU unavailable
- Continue operation when database disconnected
- Handle invalid user input gracefully
- Provide meaningful error messages

### 2. Logging
- Use structured logging for debugging
- Log performance metrics
- Record user actions for analysis
- Maintain error logs for troubleshooting

## Database Considerations

### 1. Data Models
- Use SQLAlchemy ORM for database operations
- Implement proper relationships between entities
- Handle large binary data efficiently
- Support both PostgreSQL and SQLite

### 2. Performance
- Use connection pooling for database access
- Implement efficient queries for large datasets
- Cache frequently accessed data
- Optimize database schema for signal data

## GPU Acceleration

### 1. CUDA Integration
- Use CuPy for NumPy-compatible GPU operations
- Implement fallback to CPU when CUDA unavailable
- Manage GPU memory efficiently
- Provide performance monitoring

### 2. OpenGL Visualization
- Use PyOpenGL for 3D rendering
- Implement hardware-accelerated graphics
- Handle different GPU capabilities
- Optimize rendering performance

## Configuration Management

### 1. JSON Configuration
- Store configuration in `config/` directory
- Provide example configurations
- Validate configuration files
- Support runtime configuration changes

### 2. User Preferences
- Persist user interface preferences
- Remember window layouts and settings
- Support multiple user profiles
- Export/import configuration

## Security Considerations

### 1. Data Protection
- Encrypt sensitive configuration data
- Validate all user inputs
- Protect against injection attacks
- Secure database connections

### 2. File System
- Validate file paths and permissions
- Handle file system errors gracefully
- Implement safe file operations
- Protect against path traversal attacks

## Performance Monitoring

### 1. Metrics Collection
- Monitor signal generation performance
- Track GUI responsiveness
- Measure memory usage patterns
- Log GPU utilization

### 2. Optimization
- Profile code for bottlenecks
- Optimize critical paths
- Implement caching strategies
- Use asynchronous operations where appropriate

## Documentation Requirements

### 1. Code Documentation
- Document all public APIs
- Provide usage examples
- Explain complex algorithms
- Maintain changelog

### 2. User Documentation
- Create comprehensive user manual
- Provide tutorial videos
- Document keyboard shortcuts
- Explain advanced features

## Development Workflow

### 1. Feature Development
- Start with tests (TDD approach)
- Implement minimal viable feature
- Add comprehensive error handling
- Optimize for performance

### 2. Code Review
- Review for performance implications
- Check for memory leaks
- Validate error handling
- Ensure cross-platform compatibility

### 3. Testing
- Run full test suite before commits
- Test on both Windows and Ubuntu
- Validate with different GPU configurations
- Test with various data sizes

## Common Pitfalls to Avoid

### 1. PyQt6 Issues
- Don't update GUI from worker threads
- Properly manage widget lifetimes
- Handle Qt's event system correctly
- Avoid blocking the main thread

### 2. Performance Issues
- Don't create unnecessary copies of large arrays
- Use appropriate data types (float32 vs float64)
- Implement proper caching strategies
- Monitor memory usage patterns

### 3. Database Issues
- Use transactions for data consistency
- Handle connection failures gracefully
- Optimize queries for large datasets
- Implement proper error handling

## Success Criteria

### 1. Functional Requirements
- ✅ Generate mathematical signals with configurable parameters
- ✅ Display signals in 2D, 3D, and spectral formats
- ✅ Perform real-time spectral analysis
- ✅ Persist data to database
- ✅ Support GPU acceleration

### 2. Performance Requirements
- ✅ Maintain 60+ FPS for real-time visualization
- ✅ Achieve sub-millisecond signal generation
- ✅ Complete GUI operations within 16ms
- ✅ Stable memory usage during extended operation

### 3. Quality Requirements
- ✅ 85% test coverage for mathematical modules
- ✅ 70% test coverage for GUI components
- ✅ Cross-platform compatibility (Windows/Ubuntu)
- ✅ Comprehensive error handling

Remember: This is a desktop application focused on performance and user experience. Prioritize responsiveness, accuracy, and reliability in all implementations.
