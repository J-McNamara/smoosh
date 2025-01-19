"""Repository analysis functionality for smoosh."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from .. import AnalysisError, PathLike
from ..utils.config import ConfigDict
from ..utils.file_utils import (
    find_git_root,
    get_file_size_mb,
    get_gitignore_patterns,
    walk_repository,
)
from ..utils.logger import logger


@dataclass
class FileInfo:
    """Information about a file in the repository."""

    path: Path
    relative_path: Path
    size_mb: float
    is_python: bool
    content: Optional[str] = None


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

        return generate_tree(self.root, self.files)


def analyze_repository(
    path: PathLike, config: ConfigDict, force_cat: bool = False
) -> RepositoryInfo:
    """Analyze a repository and gather information about its structure.

    Args:
        path: Path to the repository
        config: Configuration dictionary
        force_cat: Whether to force concatenation mode

    Returns:
        RepositoryInfo object containing analysis results

    Raises:
        AnalysisError: If analysis fails
    """
    path = Path(path)

    # Find git root if path is within a git repository
    git_root = find_git_root(path)
    root_path = git_root if git_root else path

    try:
        # Get gitignore patterns if respect_gitignore is enabled
        gitignore_patterns = set()
        if config["gitignore"]["respect"] and not force_cat:
            gitignore_patterns = get_gitignore_patterns(root_path)

        # Get size limit from config
        max_size_mb = config["output"]["size_limits"]["file_max_mb"]
        if force_cat:
            max_size_mb = None

        # Collect file information
        files: List[FileInfo] = []
        total_size_mb = 0
        python_files_count = 0

        logger.info(f"Analyzing repository at {root_path}")

        for file_path in walk_repository(root_path, gitignore_patterns, max_size_mb):
            try:
                # Get file info
                size_mb = get_file_size_mb(file_path)
                is_python = file_path.suffix == ".py"
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
            root=root_path,
            files=files,
            gitignore_patterns=gitignore_patterns,
            total_size_mb=total_size_mb,
            python_files_count=python_files_count,
            total_files_count=len(files),
        )

    except Exception as e:
        raise AnalysisError(f"Failed to analyze repository: {e}")


def load_file_contents(repo_info: RepositoryInfo) -> None:
    """Load the contents of all files in the repository info.

    Args:
        repo_info: Repository information object
    """
    for file_info in repo_info.files:
        try:
            with open(file_info.path, "r", encoding="utf-8") as f:
                file_info.content = f.read()
        except Exception as e:
            logger.warning(f"Error reading file {file_info.path}: {e}")
            file_info.content = None
