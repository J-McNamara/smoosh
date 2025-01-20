#!/usr/bin/env python3
"""Generate a sample Python package for testing smoosh.

This script creates a sample data science package with common patterns like:
- Data processing pipelines
- API integrations
- Configuration management
- Logging utilities
- Database operations
"""

from pathlib import Path

SAMPLE_FILES = {
    "src/sampledata/__init__.py": '''"""Sample data science package."""
from importlib.metadata import version

try:
    __version__ = version("sampledata")
except:
    __version__ = "0.1.0.dev0"
''',
    "src/sampledata/core/processor.py": '''"""Core data processing functionality."""
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path

class DataProcessor:
    """Process and transform input data."""

    def __init__(self, config: Dict[str, any]):
        """Initialize with configuration."""
        self.config = config

    def process_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply transformations to a batch of data."""
        # Common pandas operations
        df = df.dropna()
        df = df.sort_values('timestamp')

        if self.config.get('normalize'):
            df = (df - df.mean()) / df.std()

        return df

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Check if dataframe matches expected schema."""
        required = {'timestamp', 'value', 'category'}
        return required.issubset(df.columns)
''',
    "src/sampledata/api/client.py": '''"""API client for external services."""
import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """Client for external API interactions."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize client with configuration."""
        self.base_url = base_url
        self.api_key = api_key

    def get_data(self, endpoint: str, params: Dict[str, str]) -> Dict:
        """Fetch data from API endpoint."""
        headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise
''',
    "src/sampledata/db/storage.py": '''"""Database operations module."""
import sqlite3
from typing import List, Dict, Any
from pathlib import Path

class DBStorage:
    """Handle database operations."""

    def __init__(self, db_path: Path):
        """Initialize database connection."""
        self.db_path = db_path

    def store_results(self, results: List[Dict[str, Any]]) -> None:
        """Store analysis results in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results
                (id INTEGER PRIMARY KEY, timestamp TEXT, data TEXT)
            """)

            for result in results:
                cursor.execute(
                    "INSERT INTO results (timestamp, data) VALUES (?, ?)",
                    (result['timestamp'], str(result['data']))
                )
''',
    "src/sampledata/utils/config.py": '''"""Configuration management utilities."""
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        return yaml.safe_load(f)

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration structure."""
    required_keys = {'api', 'processing', 'storage'}
    return all(key in config for key in required_keys)
''',
    "tests/test_processor.py": '''"""Tests for data processor module."""
import pytest
import pandas as pd
from sampledata.core.processor import DataProcessor

def test_process_batch():
    """Test basic data processing."""
    config = {'normalize': True}
    processor = DataProcessor(config)

    df = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=3),
        'value': [1, 2, 3],
        'category': ['A', 'B', 'C']
    })

    result = processor.process_batch(df)
    assert len(result) == 3
    assert list(result.columns) == ['timestamp', 'value', 'category']

def test_validate_schema():
    """Test schema validation."""
    processor = DataProcessor({})

    valid_df = pd.DataFrame({
        'timestamp': [],
        'value': [],
        'category': []
    })
    assert processor.validate_schema(valid_df)

    invalid_df = pd.DataFrame({
        'timestamp': [],
        'value': []
    })
    assert not processor.validate_schema(invalid_df)
''',
    "pyproject.toml": """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sampledata"
version = "0.1.0"
description = "Sample package for testing smoosh"
requires-python = ">=3.8"
dependencies = [
    "pandas>=2.0.0",
    "pyyaml>=6.0.0",
    "requests>=2.0.0"
]
""",
    "README.md": """# Sample Data Package

A sample Python package demonstrating common patterns for testing smoosh.

## Features
- Data processing pipeline
- API integration
- Database operations
- Configuration management
""",
}


def generate_sample_repo(base_path: Path) -> None:
    """Generate a sample repository structure.

    Args:
    ----
        base_path: Directory where the sample repo should be created

    """
    # Create directory structure
    for file_path, content in SAMPLE_FILES.items():
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

    # Create empty __init__.py files for Python packages
    for parent in [
        "src/sampledata/core",
        "src/sampledata/api",
        "src/sampledata/db",
        "src/sampledata/utils",
        "tests",
    ]:
        init_file = base_path / parent / "__init__.py"
        init_file.parent.mkdir(parents=True, exist_ok=True)
        init_file.touch()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate sample repository for testing smoosh")
    parser.add_argument("output_dir", type=Path, help="Directory to create sample repository in")
    args = parser.parse_args()

    generate_sample_repo(args.output_dir)
    print(f"Sample repository generated in: {args.output_dir}")
