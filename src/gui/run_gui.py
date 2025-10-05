"""GUI launcher for SignalAnalyzer application."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.gui.main_window import main

if __name__ == "__main__":
    main()

