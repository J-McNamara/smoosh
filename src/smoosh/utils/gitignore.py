"""Utilities for handling .gitignore patterns."""

from pathlib import Path
from typing import List, Set
import fnmatch
import os

class GitIgnoreHandler:
    """Handles .gitignore pattern matching for file filtering."""

    DEFAULT_PYTHON_IGNORE = [
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    "*.so",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    "MANIFEST",
    ".env",
    ".venv",
    "env/",
    "venv/",
    "ENV/",
    ".pytest_cache/",
]

def __init__(self, repo_root: Path):
        """Initialize the handler with the repository root path.

        Args:
            repo_root: Path to the repository root directory
        """
        self.repo_root = repo_root
        self.ignore_patterns: List[str] = list(DEFAULT_PYTHON_IGNORE)  # Start with defaults
        self._load_gitignore()

    def should_ignore_dir(self, dir_path: Path) -> bool:
        """Quick check if a directory should be ignored (optimization).

        Args:
            dir_path: Path to directory

        Returns:
            bool: True if the directory should be skipped entirely
        """
        # Common directories we always want to ignore
        name = dir_path.name
        if name in {'__pycache__', '.git', '.pytest_cache', 'venv', '.venv', 'env'}:
            return True

        return self._is_ignored(dir_path)

def _load_gitignore(self) -> None:
        """Load patterns from .gitignore file if it exists."""
        gitignore_path = self.repo_root / '.gitignore'
        if gitignore_path.exists():
            patterns = gitignore_path.read_text().splitlines()
            # Filter out comments and empty lines
            self.ignore_patterns = [
                p.strip() for p in patterns
                if p.strip() and not p.strip().startswith('#')
            ]

    def _normalize_pattern(self, pattern: str) -> str:
        """Normalize a gitignore pattern.

        Args:
            pattern: Raw pattern from gitignore

        Returns:
            str: Normalized pattern
        """
        pattern = pattern.strip()

        # Remove any whitespace and comments
        if not pattern or pattern.startswith('#'):
            return ''

        # Handle pattern subtleties
        if pattern.startswith('!'):  # Negation not supported yet
            return ''
        if pattern.startswith('/'):  # Remove leading slashes
            pattern = pattern[1:]
        if pattern.endswith('/'):  # Keep trailing slashes for directory matches
            return pattern

        return pattern

def _is_ignored(self, path: Path) -> bool:
        """Check if a path matches any gitignore pattern.

        Args:
            path: Path to check against gitignore patterns

        Returns:
            bool: True if the path should be ignored
        """
        # Get path relative to repo root for pattern matching
        try:
            relative_path = path.relative_to(self.repo_root)
        except ValueError:
            return False

        str_path = str(relative_path).replace(os.sep, '/')

        for pattern in self.ignore_patterns:
            # Handle directory-specific patterns
            if pattern.endswith('/'):
                if self._matches_dir_pattern(str_path, pattern):
                    return True
            # Handle standard patterns
            elif fnmatch.fnmatch(current_path, pattern):
                return True
        return False

    def filter_paths(self, paths: Set[Path]) -> Set[Path]:
        """Filter out paths that match gitignore patterns.

        Args:
            paths: Set of paths to filter

        Returns:
            Set[Path]: Filtered set of paths
        """
        if not self.ignore_patterns:
            return paths

        return {
            path for path in paths
            if not self._is_ignored(path)
        }fnmatch(str_path, pattern):
                return True
        return False

    def _matches_dir_pattern(self, path: str, pattern: str) -> bool:
        """Check if path matches a directory-specific pattern.

        Args:
            path: Path string to check
            pattern: Directory pattern from .gitignore

        Returns:
            bool: True if the path matches the directory pattern
        """
        # Remove trailing slash from pattern
        pattern = pattern.rstrip('/')

        # Check if path or any of its parent directories match
        path_parts = path.split('/')
        for i in range(len(path_parts)):
            current_path = '/'.join(path_parts[:i + 1])
            if fnmatch.
