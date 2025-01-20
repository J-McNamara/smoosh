"""Repository content composition functionality for smoosh."""

from typing import Dict, Tuple, Union

from .. import GenerationError
from ..analyzer.repository import RepositoryInfo, load_file_contents
from ..utils.config import ConfigDict
from ..utils.logger import logger


class CompositionError(GenerationError):
    """Raised when composition fails."""

    pass


def concatenate_files(
    repo_info: RepositoryInfo, mode: str, config: ConfigDict
) -> Tuple[str, Dict[str, Union[str, int]]]:
    """Compose repository files into a single coherent representation.

    Args:
    ----
        repo_info: Repository information
        mode: Composition mode ('cat', 'fold', or 'smoosh')
        config: Configuration dictionary

    Returns:
    -------
        Tuple of (composed content, statistics dictionary)

    Raises:
    ------
        CompositionError: If composition fails

    """
    try:
        # Load file contents if not already loaded
        load_file_contents(repo_info)

        # Compose the parts
        header = compose_header(repo_info, mode)
        content = compose_content(repo_info, mode)
        stats = gather_statistics(repo_info, content)

        # Combine all parts
        full_composition = f"{header}\n\n{content}"

        # Check against max tokens if configured
        max_tokens = config["output"].get("max_tokens")
        if max_tokens and len(full_composition.split()) > max_tokens:
            logger.warning(
                f"Composition exceeds max_tokens ({max_tokens}). "
                "Consider using a different mode or adjusting the limit."
            )

        return full_composition, stats

    except Exception as e:
        raise CompositionError(f"Failed to compose repository content: {e}") from e


def compose_header(repo_info: RepositoryInfo, mode: str) -> str:
    """Compose the header section.

    Args:
    ----
        repo_info: Repository information
        mode: Composition mode

    Returns:
    -------
        Composed header string

    """
    header = [
        f"Repository: {repo_info.root.name}",
        f"Mode: {mode}",
        f"Files: {repo_info.total_files_count} ({repo_info.python_files_count} Python)",
        f"Total Size: {repo_info.total_size_mb:.2f}MB",
        "",
        "Repository Structure:",
        repo_info.get_tree_representation(),
    ]

    return "\n".join(header)


def compose_content(repo_info: RepositoryInfo, mode: str) -> str:
    """Compose the main content based on the specified mode.

    Args:
    ----
        repo_info: Repository information
        mode: Composition mode

    Returns:
    -------
        Composed content string

    """
    if mode == "cat":
        return compose_cat_mode(repo_info)
    elif mode == "fold":
        return compose_fold_mode(repo_info)
    elif mode == "smoosh":
        return compose_smoosh_mode(repo_info)
    else:
        raise CompositionError(f"Unknown composition mode: {mode}")


def compose_cat_mode(repo_info: RepositoryInfo) -> str:
    """Compose content in full concatenation mode.

    Args:
    ----
        repo_info: Repository information

    Returns:
    -------
        Concatenated content

    """
    sections = []

    for file_info in repo_info.files:
        if file_info.content is None:
            continue

        sections.extend(["", f"### File: {file_info.relative_path} ###", file_info.content])

    return "\n".join(sections)


def compose_fold_mode(repo_info: RepositoryInfo) -> str:
    """Compose content in structure-preserving mode (placeholder).

    Args:
    ----
        repo_info: Repository information

    Returns:
    -------
        Structure-preserved content

    """
    # TODO: Implement fold mode composition
    return compose_cat_mode(repo_info)


def compose_smoosh_mode(repo_info: RepositoryInfo) -> str:
    """Compose content in maximum compression mode (placeholder).

    Args:
    ----
        repo_info: Repository information

    Returns:
    -------
        Compressed content

    """
    # TODO: Implement smoosh mode composition
    return compose_cat_mode(repo_info)


def gather_statistics(repo_info: RepositoryInfo, content: str) -> Dict[str, Union[str, int]]:
    """Gather statistics about the composed content.

    Args:
    ----
        repo_info: Repository information
        content: Composed content

    Returns:
    -------
        Dictionary of statistics

    """
    # Calculate original sizes
    original_lines = sum(
        len(f.content.splitlines()) for f in repo_info.files if f.content is not None
    )
    original_chars = sum(len(f.content) for f in repo_info.files if f.content is not None)

    # Calculate composition sizes
    composed_lines = len(content.splitlines())
    composed_chars = len(content)

    return {
        "Repository Size": f"{repo_info.total_size_mb:.2f}MB",
        "Total Files": repo_info.total_files_count,
        "Python Files": repo_info.python_files_count,
        "Original Lines": original_lines,
        "Composed Lines": composed_lines,
        "Original Characters": original_chars,
        "Composed Characters": composed_chars,
        "Lines Ratio": (f"{composed_lines / original_lines:.2f}x" if original_lines else "N/A"),
        "Characters Ratio": (
            f"{composed_chars / original_chars:.2f}x" if original_chars else "N/A"
        ),
    }
