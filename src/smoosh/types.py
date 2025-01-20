"""Type definitions for smoosh."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FileInfo:
    """Information about a file in the repository."""

    path: Path
    relative_path: Path
    size_mb: float = 0.0
    is_python: bool = False
    content: Optional[str] = None
