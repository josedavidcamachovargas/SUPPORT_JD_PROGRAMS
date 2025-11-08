#!/usr/bin/env python3
"""
Activity Selector - Cross-platform launcher
This script works on both Windows and Ubuntu/Linux
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import and run the main application
if __name__ == "__main__":
    from activity_selector_refactored import main
    main()
