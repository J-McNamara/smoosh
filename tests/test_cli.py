"""Test suite for the smoosh CLI."""

from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner

from smoosh.cli import analyze, main, structure, summarize


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


def test_analyze_command(runner: CliRunner, temp_package: Path) -> None:
    """Test the analyze command.

    Args:
        runner: Click CLI test runner
        temp_package: Path to temporary test package
    """
    result = runner.invoke(analyze, [str(temp_package)])
    assert result.exit_code == 0
    assert "Analyzing package" in result.output
    assert "Analysis complete!" in result.output


def test_summarize_command(runner: CliRunner, temp_package: Path) -> None:
    """Test the summarize command.

    Args:
        runner: Click CLI test runner
        temp_package: Path to temporary test package
    """
    result = runner.invoke(summarize, [str(temp_package)])
    assert result.exit_code == 0
    assert "Summarizing package" in result.output
    assert "Coming soon!" in result.output


def test_structure_command(runner: CliRunner, temp_package: Path) -> None:
    """Test the structure command.

    Args:
        runner: Click CLI test runner
        temp_package: Path to temporary test package
    """
    result = runner.invoke(structure, [str(temp_package)])
    assert result.exit_code == 0
    assert "Analyzing structure" in result.output
    assert "Coming soon!" in result.output


def test_invalid_path(runner: CliRunner) -> None:
    """Test handling of invalid paths.

    Args:
        runner: Click CLI test runner
    """
    result = runner.invoke(analyze, ["nonexistent_path"])
    assert result.exit_code == 2
    assert "Path 'nonexistent_path' does not exist" in result.output
