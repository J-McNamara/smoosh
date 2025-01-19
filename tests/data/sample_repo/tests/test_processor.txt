"""Tests for data processor module."""
import pandas as pd
import pytest
from sampledata.core.processor import DataProcessor


def test_process_batch():
    """Test basic data processing."""
    config = {"normalize": True}
    processor = DataProcessor(config)

    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=3),
            "value": [1, 2, 3],
            "category": ["A", "B", "C"],
        }
    )

    result = processor.process_batch(df)
    assert len(result) == 3
    assert list(result.columns) == ["timestamp", "value", "category"]


def test_validate_schema():
    """Test schema validation."""
    processor = DataProcessor({})

    valid_df = pd.DataFrame({"timestamp": [], "value": [], "category": []})
    assert processor.validate_schema(valid_df)

    invalid_df = pd.DataFrame({"timestamp": [], "value": []})
    assert not processor.validate_schema(invalid_df)
