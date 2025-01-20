"""File handling utilities for smoosh."""

import fnmatch
import os
from pathlib import Path
from typing import Iterator, Optional, Set, Union

import chardet

# Define a more specific PathLike type that only includes str paths
PathLike = Union[str, "os.PathLike[str]"]

# Default Python patterns that should always be ignored
DEFAULT_PYTHON_IGNORE = {
    # Python bytecode
    "**/__pycache__/",
    "**/*.py[cod]",
    "**/*$py.class",
    "**/*.so",
    # Distribution/packaging
    "**/build/",
    "**/dist/",
    "**/*.egg-info/",
    "**/eggs/",
    "**/.eggs/",
    # Virtual environments
    "**/.env/",
    "**/.venv/",
    "**/env/",
    "**/venv/",
    # Testing and coverage
    "**/.pytest_cache/",
    "**/.coverage",
    "**/htmlcov/",
    "**/.tox/",
    # Type checking
    "**/.mypy_cache/",
    "**/.pytype/",
    # IDE
    "**/.idea/",
    "**/.vscode/",
    "**/*.swp",
    # Version control
    "**/.git/",
    "**/.git",
    "**/.hg/",
    "**/.svn/",
    # Misc
    "**/node_modules/",
    "**/.DS_Store",
}


def is_text_file(path: PathLike) -> bool:
    """Check if a file is a text file by analyzing its content.

    Args:
    ----
        path: Path to the file

    Returns:
    -------
        True if the file appears to be text, False otherwise

    """
    try:
        with open(str(path), "rb") as f:
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
    ----
        path: Path to the file

    Returns:
    -------
        File size in MB

    """
    return os.path.getsize(str(path)) / (1024 * 1024)


def find_git_root(start_path: PathLike) -> Optional[Path]:
    """Find the root of the git repository containing start_path.

    Args:
    ----
        start_path: Path to start searching from

    Returns:
    -------
        Path to git root if found, None otherwise

    """
    # Convert to Path, ensuring str type
    start_path = Path(str(start_path)).resolve()

    # Handle if start_path is a file
    if start_path.is_file():
        start_path = start_path.parent

    current = start_path
    while current != current.parent:
        if (current / ".git").is_dir():
            return current
        current = current.parent
    return None


def _normalize_pattern(pattern: str) -> str:
    """Normalize a gitignore pattern.

    Args:
    ----
        pattern: Raw pattern from gitignore

    Returns:
    -------
        Normalized pattern or empty string if invalid

    """
    pattern = pattern.strip()

    # Skip empty lines and comments
    if not pattern or pattern.startswith("#"):
        return ""

    # Skip negation patterns for now
    if pattern.startswith("!"):
        return ""

    # Remove leading slashes
    if pattern.startswith("/"):
        pattern = pattern[1:]

    return pattern


def get_gitignore_patterns(repo_root: PathLike) -> Set[str]:
    """Get patterns from .gitignore file.

    Args:
    ----
        repo_root: Repository root path

    Returns:
    -------
        Set of gitignore patterns

    """
    patterns = set(DEFAULT_PYTHON_IGNORE)  # Start with default patterns
    gitignore_path = Path(str(repo_root)) / ".gitignore"

    if gitignore_path.is_file():
        with open(gitignore_path, encoding="utf-8") as f:
            for line in f:
                pattern = _normalize_pattern(line)
                if pattern:
                    patterns.add(pattern)

    return patterns


def should_ignore_path(path: Path, relative_to: Path, ignore_patterns: Set[str]) -> bool:
    """Check if a path should be ignored based on gitignore patterns.

    Args:
    ----
        path: Path to check
        relative_to: Repository root path to make path relative to
        ignore_patterns: Set of patterns to check against

    Returns:
    -------
        True if path should be ignored

    """
    # Quick check for common ignored directories
    if path.name in {"__pycache__", ".git", ".pytest_cache", "venv", ".env", "env"}:
        return True

    # Get path relative to repo root
    try:
        rel_path = str(path.relative_to(relative_to))
    except ValueError:
        return False

    # Normalize path separators
    rel_path = rel_path.replace(os.sep, "/")

    # Check against patterns
    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            # Directory matching
            if any(fnmatch.fnmatch(part, pattern[:-1]) for part in path.parts):
                return True
        else:
            # File matching
            if fnmatch.fnmatch(rel_path, pattern):
                return True

    return False


def walk_repository(
    root: PathLike, ignore_patterns: Optional[Set[str]] = None, max_size_mb: Optional[float] = None
) -> Iterator[Path]:
    """Walk through repository yielding relevant files.

    Args:
    ----
        root: Repository root path
        ignore_patterns: Set of patterns to ignore
        max_size_mb: Maximum file size in MB

    Yields:
    ------
        Path objects for each relevant file

    """
    root = Path(str(root))
    ignore_patterns = ignore_patterns or set()

    for path in root.rglob("*"):
        # Skip ignored paths
        if should_ignore_path(path, root, ignore_patterns):
            continue

        # Skip directories
        if path.is_dir():
            continue

        # Skip files exceeding size limit
        if max_size_mb and get_file_size_mb(path) > max_size_mb:
            continue

        # Skip non-text files
        if not is_text_file(path):
            continue

        yield path
