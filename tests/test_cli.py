"""Test suite for the smoosh CLI."""

from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner

from smoosh.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Click CLI test runner.

    Returns:
        CliRunner: A Click test runner instance
    """
    return CliRunner()


@pytest.fixture
def temp_package(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary Python package for testing.

    Args:
        tmp_path: Pytest fixture providing temporary directory path

    Yields:
        Path: Path to temporary directory containing the test package
    """
    # Create a minimal Python package
    pkg_dir = tmp_path / "sample_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    yield tmp_path


def test_main_shows_help(runner: CliRunner) -> None:
    """Test that the main command shows help text.

    Args:
        runner: Click CLI test runner
    """
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Smoosh Python packages into digestible summaries" in result.output
