"""Directory tree generation functionality for smoosh."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union

from ..custom_types import FileInfo

# Define PathLike type consistently with file_utils
PathLike = Union[str, "os.PathLike[str]"]


@dataclass
class TreeNode:
    """Node in the directory tree."""

    name: str
    is_dir: bool
    children: Dict[str, "TreeNode"]
    is_python: bool = False

    def __init__(self, name: str, is_dir: bool = True):
        """Initialize a TreeNode.

        Args:
        ----
            name: Name of the node (file or directory)
            is_dir: Whether the node represents a directory
        """
        self.name = name
        self.is_dir = is_dir
        self.children = {}
        self.is_python = name.endswith(".py")


def build_tree(root: PathLike, files: List[FileInfo]) -> TreeNode:
    """Build a tree structure from list of files.

    Args:
    ----
        root: Repository root path
        files: List of FileInfo objects

    Returns:
    -------
        TreeNode representing the root of the tree

    """
    # Convert root path to string safely
    root_path = Path(str(root))
    root_name = root_path.name or str(root_path)
    root_node = TreeNode(root_name)

    for file_info in files:
        current = root_node
        parts = file_info.relative_path.parts

        # Create directory nodes
        for part in parts[:-1]:
            if part not in current.children:
                current.children[part] = TreeNode(part)
            current = current.children[part]

        # Create file node
        file_name = parts[-1]
        current.children[file_name] = TreeNode(name=file_name, is_dir=False)

    return root_node


def format_tree(
    node: TreeNode,
    prefix: str = "",
    is_last: bool = True,
    include_indicators: bool = True,
) -> str:
    """Format a tree node as a string.

    Args:
    ----
        node: Tree node to format
        prefix: Prefix for current line
        is_last: Whether this is the last child of its parent
        include_indicators: Whether to include file type indicators

    Returns:
    -------
        Formatted string representation of the tree

    """
    # Sort children: directories first, then files, both alphabetically
    sorted_children = sorted(node.children.items(), key=lambda x: (not x[1].is_dir, x[0].lower()))

    # Prepare the current line
    if node.is_dir:
        name = f"{node.name}/"
    else:
        name = node.name

    # Build the line with proper prefixes
    if prefix:
        line = prefix + ("└── " if is_last else "├── ") + name + "\n"
    else:
        line = name + "\n"

    # Process children
    children_count = len(sorted_children)
    for i, (_, child_node) in enumerate(sorted_children):  # Removed unused `child_name`
        child_prefix = prefix + ("    " if is_last else "│   ")
        line += format_tree(child_node, child_prefix, i == children_count - 1, include_indicators)

    return line


def generate_tree(root: PathLike, files: List[FileInfo]) -> str:
    """Compose a tree representation of the repository structure.

    Args:
    ----
        root: Repository root path
        files: List of FileInfo objects

    Returns:
    -------
        String representation of the directory tree

    """
    tree = build_tree(root, files)
    return format_tree(tree)
