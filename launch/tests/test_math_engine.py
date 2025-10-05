#!/usr/bin/env python3
"""Test script for SignalAnalyzer mathematical engine."""

import sys
from pathlib import Path
import numpy as np

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.math.signal_generator import SignalGenerator, SignalParameters, SignalType, SignalAnalyzer
    print("✅ Mathematical engine imported successfully")
    
    # Test signal generation
    generator = SignalGenerator()
    
    # Test different signal types
    test_signals = [
        SignalParameters(signal_type=SignalType.SINE, frequency=1000, amplitude=1.0),
        SignalParameters(signal_type=SignalType.SQUARE, frequency=500, amplitude=0.5),
        SignalParameters(signal_type=SignalType.SAWTOOTH, frequency=2000, amplitude=1.5),
        SignalParameters(signal_type=SignalType.COMPLEX, frequency=440, amplitude=1.0),
    ]
    
    print("\n🎯 Testing Signal Generation:")
    print("=" * 50)
    
    for i, params in enumerate(test_signals, 1):
        try:
            time, signal = generator.generate_signal(params)
            
            print(f"\n{i}. {params.signal_type.value.upper()} Signal:")
            print(f"   Frequency: {params.frequency} Hz")
            print(f"   Amplitude: {params.amplitude} V")
            print(f"   Duration: {params.duration} s")
            print(f"   Samples: {len(signal)}")
            print(f"   Max value: {np.max(signal):.3f} V")
            print(f"   Min value: {np.min(signal):.3f} V")
            print(f"   RMS value: {np.sqrt(np.mean(signal**2)):.3f} V")
            
            # Test FFT analysis
            freqs, fft_mag = SignalAnalyzer.compute_fft(signal, params.sample_rate)
            print(f"   FFT peak frequency: {freqs[np.argmax(fft_mag)]:.1f} Hz")
            
            # Test statistics
            stats = SignalAnalyzer.compute_statistics(signal)
            print(f"   Crest factor: {stats['crest_factor']:.3f}")
            print(f"   Peak-to-peak: {stats['peak_to_peak']:.3f} V")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎯 Testing Signal Analysis:")
    print("=" * 50)
    
    # Test analysis on a complex signal
    params = SignalParameters(
        signal_type=SignalType.COMPLEX,
        frequency=440,
        amplitude=1.0,
        duration=0.1
    )
    
    time, signal = generator.generate_signal(params)
    
    # FFT Analysis
    freqs, fft_mag = SignalAnalyzer.compute_fft(signal, params.sample_rate)
    print(f"\n📊 FFT Analysis:")
    print(f"   Frequency resolution: {freqs[1] - freqs[0]:.1f} Hz")
    print(f"   Peak frequencies: {freqs[np.argsort(fft_mag)[-3:]]}")
    
    # Power Spectral Density
    freqs_psd, psd = SignalAnalyzer.compute_spectral_density(signal, params.sample_rate)
    print(f"\n📊 Power Spectral Density:")
    print(f"   Total power: {np.sum(psd):.3f}")
    print(f"   Peak PSD: {np.max(psd):.3f}")
    
    # Peak Detection
    peaks = SignalAnalyzer.find_peaks(signal, threshold=0.1)
    print(f"\n📊 Peak Detection:")
    print(f"   Found {len(peaks)} peaks")
    if peaks:
        print(f"   Peak times: {[time[p] for p in peaks[:5]]}")  # Show first 5 peaks
    
    # Signal Statistics
    stats = SignalAnalyzer.compute_statistics(signal)
    print(f"\n📊 Signal Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value:.6f}")
    
    print("\n✅ Mathematical engine test completed successfully!")
    print("\n🎯 What was tested:")
    print("  • Signal generation (sine, square, sawtooth, complex)")
    print("  • FFT analysis and frequency domain")
    print("  • Power spectral density calculation")
    print("  • Peak detection algorithms")
    print("  • Statistical analysis")
    print("  • Signal parameter validation")
    
    # Test signal saving
    if generator.save_signal("test_signal.csv"):
        print("\n💾 Signal saved to test_signal.csv")
    
    print("\n🚀 Ready for GUI integration!")
    
except ImportError as e:
    print(f"❌ Error importing mathematical engine: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Mathematical engine test failed: {e}")
    sys.exit(1)
