"""Tests for output format handling."""

from typing import Any, Dict, List

import pytest

from smoosh.generator.formats import format_output  # assuming this is the function we're testing

# Test data representing a sample package summary
TEST_DATA: List[Dict[str, Any]] = [
    {
        "name": "example_package",
        "structure": {
            "modules": ["core", "utils", "api"],
            "patterns": {"p1": "DataFrame processor", "p2": "Data validation"},
        },
        "api": {
            "core": [
                "process_data(df: DataFrame) -> DataFrame",
                "validate_input(data: Dict[str, Any]) -> bool",
            ],
            "utils": ["load_config(path: str) -> Config"],
        },
    }
]


def test_format_output_json() -> None:
    """Test JSON format output generation."""
    result = format_output(TEST_DATA, format_type="json")
    assert isinstance(result, str)
    assert "example_package" in result
    assert "DataFrame processor" in result


def test_format_output_yaml() -> None:
    """Test YAML format output generation."""
    result = format_output(TEST_DATA, format_type="yaml")
    assert isinstance(result, str)
    assert "example_package" in result
    assert "modules:" in result


def test_format_output_markdown() -> None:
    """Test Markdown format output generation."""
    result = format_output(TEST_DATA, format_type="markdown")
    assert isinstance(result, str)
    assert "# example_package" in result
    assert "## Structure" in result


def test_format_output_llm() -> None:
    """Test LLM format output generation."""
    result = format_output(TEST_DATA, format_type="llm")
    assert isinstance(result, str)
    assert "Package Summary:" in result
    assert "Key Components:" in result


def test_format_output_invalid_format() -> None:
    """Test handling of invalid format type."""
    with pytest.raises(ValueError) as exc_info:
        format_output(TEST_DATA, format_type="invalid")
    assert "Unsupported format type" in str(exc_info.value)


def test_format_output_empty_data() -> None:
    """Test handling of empty input data."""
    with pytest.raises(ValueError) as exc_info:
        format_output([], format_type="json")
    assert "Empty input data" in str(exc_info.value)


def test_format_output_malformed_data() -> None:
    """Test handling of malformed input data."""
    malformed_data = [{"incomplete": "data"}]
    with pytest.raises(ValueError) as exc_info:
        format_output(malformed_data, format_type="json")
    assert "Invalid input data structure" in str(exc_info.value)
