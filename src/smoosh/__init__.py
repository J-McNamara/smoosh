"""smoosh - Software Module Outline & Organization Summary Helper."""

import os
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Dict, Union

try:
    __version__ = version("smoosh")
except PackageNotFoundError:
    __version__ = "0.1.0"  # Default during development

__author__ = "Joshua T. McNamara"
__license__ = "MIT"

# Type aliases for clarity
PathLike = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]
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
