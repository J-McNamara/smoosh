"""Repository analysis functionality for smoosh."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Union

from ..custom_types import FileInfo
from ..utils.config import ConfigDict
from ..utils.file_utils import (
    find_git_root,
    get_file_size_mb,
    get_gitignore_patterns,
    walk_repository,
)
from ..utils.logger import logger

# Define PathLike type consistently with other modules
PathLike = Union[str, "os.PathLike[str]"]


@dataclass
class RepositoryInfo:
    """Information about the analyzed repository."""

    root: Path
    files: List[FileInfo]
    gitignore_patterns: Set[str]
    total_size_mb: float
    python_files_count: int
    total_files_count: int

    def get_tree_representation(self) -> str:
        """Compose a tree-style representation of the repository structure."""
        from .tree import generate_tree

        return generate_tree(str(self.root), self.files)


def analyze_repository(
    path: PathLike, config: ConfigDict, force_cat: bool = False
) -> RepositoryInfo:
    """Analyze a repository and gather information about its structure.

    Args:
    ----
        path: Path to the repository
        config: Configuration dictionary
        force_cat: Whether to force concatenation mode

    Returns:
    -------
        RepositoryInfo object containing analysis results

    Raises:
    ------
        AnalysisError: If analysis fails

    """
    input_path = Path(str(path))

    # Determine whether to use git root or provided path
    git_root = find_git_root(input_path)
    is_git_root = bool(git_root and git_root == input_path)

    # Use git root only if the provided path is the repo root
    root_path = input_path  # Default to input path
    if is_git_root and git_root:
        logger.info(f"Git repository root detected at {input_path}")
        root_path = git_root
    else:
        logger.info(f"Processing directory at {input_path}")

    try:
        # Get gitignore patterns if respect_gitignore is enabled
        gitignore_patterns: Set[str] = set()
        if config["gitignore"]["respect"] and not force_cat:
            # Still get gitignore from git root if available for pattern matching
            gitignore_root = git_root if git_root else root_path
            # Convert Path to str for gitignore pattern retrieval
            gitignore_patterns = get_gitignore_patterns(str(gitignore_root))

        # Always exclude the .git directory
        gitignore_patterns.add(".git/")

        # Get size limit from config
        max_size_mb: Optional[float] = (
            None if force_cat else config["output"]["size_limits"]["file_max_mb"]
        )

        # Collect file information
        files: List[FileInfo] = []
        total_size_mb: float = 0.0
        python_files_count: int = 0

        # Convert root_path to str for walk_repository
        for file_path in walk_repository(str(root_path), gitignore_patterns, max_size_mb):
            try:
                # Get file info
                size_mb = get_file_size_mb(file_path)
                is_python = file_path.suffix == ".py"
                # We know root_path is a Path here
                relative_path = file_path.relative_to(root_path)

                file_info = FileInfo(
                    path=file_path,
                    relative_path=relative_path,
                    size_mb=size_mb,
                    is_python=is_python,
                )

                files.append(file_info)
                total_size_mb += size_mb
                if is_python:
                    python_files_count += 1

            except Exception as e:
                logger.warning(f"Error processing file {file_path}: {e}")

        # Sort files by relative path for consistent ordering
        files.sort(key=lambda f: str(f.relative_path))

        return RepositoryInfo(
            root=root_path,  # root_path is now guaranteed to be a Path
            files=files,
            gitignore_patterns=gitignore_patterns,
            total_size_mb=total_size_mb,
            python_files_count=python_files_count,
            total_files_count=len(files),
        )

    except Exception as e:
        raise AnalysisError(f"Failed to analyze repository: {e}") from e


def load_file_contents(repo_info: RepositoryInfo) -> None:
    """Load the contents of all files in the repository info.

    Args:
    ----
        repo_info: Repository information object

    """
    for file_info in repo_info.files:
        try:
            with open(file_info.path, encoding="utf-8") as f:
                file_info.content = f.read()
        except Exception as e:
            logger.warning(f"Error reading file {file_info.path}: {e}")
            file_info.content = None


class AnalysisError(Exception):
    """Raised when repository analysis fails."""

    pass
