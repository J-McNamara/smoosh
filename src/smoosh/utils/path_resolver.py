"""Path resolution utilities for smoosh."""

import site
import sys
from importlib import util
from pathlib import Path
from typing import Optional

from ..utils.logger import logger


def find_package_path(package_name: str) -> Optional[Path]:
    """Find the installation path of a Python package.

    Args:
    ----
        package_name: Name of the package to find

    Returns:
    -------
        Path to the package directory if found, None otherwise

    """
    # Try direct spec lookup first
    spec = util.find_spec(package_name)
    if spec and spec.origin:
        # Get package directory from module file
        package_path = Path(spec.origin).parent
        if package_path.is_dir():
            return package_path

    # Search common site-packages locations
    search_paths = sys.path + site.getsitepackages()
    if site.getusersitepackages():
        search_paths.append(site.getusersitepackages())

    for path in search_paths:
        package_path = Path(path) / package_name
        if package_path.is_dir() and (package_path / "__init__.py").exists():
            return package_path

    return None


def resolve_path(path_or_name: str) -> Path:
    """Resolve a path or package name to a filesystem path.

    Args:
    ----
        path_or_name: Either a filesystem path or package name

    Returns:
    -------
        Resolved filesystem path

    Raises:
    ------
        FileNotFoundError: If path doesn't exist and package cannot be found

    """
    # First try as direct path
    direct_path = Path(path_or_name)
    if direct_path.exists():
        return direct_path

    # Try as package name
    package_path = find_package_path(path_or_name)
    if package_path:
        logger.info(f"Found package '{path_or_name}' at {package_path}")
        return package_path

    raise FileNotFoundError(
        f"Could not find path or package '{path_or_name}'. "
        "Please provide a valid filesystem path or installed package name."
    )
