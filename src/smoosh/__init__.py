"""
smoosh - Software Module Outline & Organization Summary Helper
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("smoosh")
except PackageNotFoundError:
    __version__ = "0.1.0.dev0"  # Default during development

__author__ = "Project Contributors"
__license__ = "MIT"

from typing import Any, Dict, List, Optional, Union

# Type aliases for clarity
PathLike = Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"]
ConfigDict = Dict[str, Any]


# Exception classes
class SmooshError(Exception):
    """Base exception class for smoosh."""

    pass


class ConfigurationError(SmooshError):
    """Raised when there's an error in configuration."""

    pass


class AnalysisError(SmooshError):
    """Raised when analysis fails."""

    pass


class GenerationError(SmooshError):
    """Base class for composition errors."""

    pass
