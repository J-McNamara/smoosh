"""Core data processing functionality."""
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


class DataProcessor:
    """Process and transform input data."""

    def __init__(self, config: Dict[str, any]):
        """Initialize with configuration."""
        self.config = config

    def process_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply transformations to a batch of data."""
        # Common pandas operations
        df = df.dropna()
        df = df.sort_values("timestamp")

        if self.config.get("normalize"):
            df = (df - df.mean()) / df.std()

        return df

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Check if dataframe matches expected schema."""
        required = {"timestamp", "value", "category"}
        return required.issubset(df.columns)
