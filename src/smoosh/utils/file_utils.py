"""File handling utilities for smoosh."""

import os
from pathlib import Path
from typing import Iterator, List, Optional, Set, Union

import chardet

# Define PathLike here instead of importing from parent
PathLike = Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"]


def is_text_file(path: PathLike) -> bool:
    """Check if a file is a text file by analyzing its content.

    Args:
        path: Path to the file

    Returns:
        True if the file appears to be text, False otherwise
    """
    try:
        with open(path, "rb") as f:
            # Read first 1024 bytes for detection
            sample = f.read(1024)
            if not sample:  # Empty file
                return True

            # Try to detect encoding
            result = chardet.detect(sample)
            if result["encoding"] is None:
                return False

            # Check if file can be decoded as text
            sample.decode(result["encoding"])
            return True
    except (UnicodeDecodeError, OSError):
        return False


def get_file_size_mb(path: PathLike) -> float:
    """Get file size in megabytes.

    Args:
        path: Path to the file

    Returns:
        File size in MB
    """
    return os.path.getsize(path) / (1024 * 1024)


def find_git_root(start_path: PathLike) -> Optional[Path]:
    """Find the root of the git repository containing start_path.

    Args:
        start_path: Path to start searching from

    Returns:
        Path to git root if found, None otherwise
    """
    start_path = Path(start_path).resolve()

    # Handle if start_path is a file
    if start_path.is_file():
        start_path = start_path.parent

    current = start_path
    while current != current.parent:
        if (current / ".git").is_dir():
            return current
        current = current.parent
    return None


def get_gitignore_patterns(repo_root: PathLike) -> Set[str]:
    """Get patterns from .gitignore file.

    Args:
        repo_root: Repository root path

    Returns:
        Set of gitignore patterns
    """
    patterns = set()
    gitignore_path = Path(repo_root) / ".gitignore"

    if gitignore_path.is_file():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.add(line)

    return patterns


def walk_repository(
    root: PathLike, ignore_patterns: Optional[Set[str]] = None, max_size_mb: Optional[float] = None
) -> Iterator[Path]:
    """Walk through repository yielding relevant files.

    Args:
        root: Repository root path
        ignore_patterns: Set of patterns to ignore
        max_size_mb: Maximum file size in MB

    Yields:
        Path objects for each relevant file
    """
    root = Path(root)
    ignore_patterns = ignore_patterns or set()

    for path in root.rglob("*"):
        # Skip directories
        if path.is_dir():
            continue

        # Skip files matching ignore patterns
        if any(path.match(pattern) for pattern in ignore_patterns):
            continue

        # Skip files exceeding size limit
        if max_size_mb and get_file_size_mb(path) > max_size_mb:
            continue

        # Skip non-text files
        if not is_text_file(path):
            continue

        yield path
