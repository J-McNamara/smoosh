"""Test configuration and fixtures for smoosh.

This module contains shared fixtures and configuration for the smoosh test suite.
It ensures proper path handling and test discovery.
"""

import os
import sys
from typing import List

# Add the src directory to the Python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Configure pytest to discover tests relative to this directory
pytest_plugins: List[str] = []
