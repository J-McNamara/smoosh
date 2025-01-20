"""Test suite for the smoosh CLI."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from smoosh.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Click CLI test runner.

    Returns:
    -------
        CliRunner: A Click test runner instance

    """
    return CliRunner()


@pytest.fixture
def temp_package(tmp_path: Path) -> Path:
    """Create a temporary Python package for testing.

    Args:
    ----
        tmp_path: Pytest fixture providing temporary directory path

    Returns:
    -------
        Path: Path to temporary directory containing the test package

    """
    # Create a minimal Python package
    pkg_dir = tmp_path / "sample_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    return pkg_dir


def test_main_shows_help(runner: CliRunner) -> None:
    """Test that the main command shows help text.

    Args:
    ----
        runner: Click CLI test runner

    """
    result = runner.invoke(main, ["--help"])
    expected_text = "Smoosh software packages into plaintext summaries on the clipboard"

    if result.exit_code != 0:
        pytest.fail("CLI should exit successfully")
    if expected_text not in result.output:
        pytest.fail("Help text should contain package description")
