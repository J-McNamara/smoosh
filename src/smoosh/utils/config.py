"""Configuration handling for smoosh."""

import os
from pathlib import Path
from typing import Any, Dict, TypedDict, Union

import yaml

from .. import ConfigurationError  # Import the exception from root package

# Define PathLike type consistently with other modules
PathLike = Union[str, "os.PathLike[str]"]


class SizeLimitsDict(TypedDict):
    """TypedDict for size limits configuration."""

    file_max_mb: float


class OutputDict(TypedDict):
    """TypedDict for output configuration."""

    max_tokens: int
    size_limits: SizeLimitsDict


class ThresholdsDict(TypedDict):
    """TypedDict for thresholds configuration."""

    cat_threshold: int
    fold_threshold: int


class GitignoreDict(TypedDict):
    """TypedDict for gitignore configuration."""

    respect: bool


class ConfigDict(TypedDict):
    """TypedDict for the overall configuration."""

    output: OutputDict
    thresholds: ThresholdsDict
    gitignore: GitignoreDict


DEFAULT_CONFIG: ConfigDict = {
    "output": {"max_tokens": 5000, "size_limits": {"file_max_mb": 1.0}},
    "thresholds": {"cat_threshold": 5000, "fold_threshold": 15000},
    "gitignore": {"respect": True},
}


def _merge_output(base_output: OutputDict, update_output: Dict[str, Any]) -> OutputDict:
    """Merge output section of configuration."""
    output_dict = base_output.copy()
    if "max_tokens" in update_output:
        output_dict["max_tokens"] = update_output["max_tokens"]
    if "size_limits" in update_output and isinstance(update_output["size_limits"], dict):
        size_limits = output_dict["size_limits"].copy()
        if "file_max_mb" in update_output["size_limits"]:
            size_limits["file_max_mb"] = update_output["size_limits"]["file_max_mb"]
        output_dict["size_limits"] = size_limits
    return output_dict


def _merge_thresholds(
    base_thresholds: ThresholdsDict, update_thresholds: Dict[str, Any]
) -> ThresholdsDict:
    """Merge thresholds section of configuration."""
    thresholds_dict = base_thresholds.copy()
    if "cat_threshold" in update_thresholds:
        thresholds_dict["cat_threshold"] = update_thresholds["cat_threshold"]
    if "fold_threshold" in update_thresholds:
        thresholds_dict["fold_threshold"] = update_thresholds["fold_threshold"]
    return thresholds_dict


def _merge_gitignore(
    base_gitignore: GitignoreDict, update_gitignore: Dict[str, Any]
) -> GitignoreDict:
    """Merge gitignore section of configuration."""
    gitignore_dict = base_gitignore.copy()
    if "respect" in update_gitignore:
        gitignore_dict["respect"] = update_gitignore["respect"]
    return gitignore_dict


def load_config(config_dir: Path) -> Dict[str, Any]:
    """Load configuration from smoosh.yaml in the specified directory.

    Args:
        config_dir: Directory containing the configuration file

    Returns:
        Configuration dictionary with defaults

    Raises:
        ConfigurationError: If configuration loading fails
    """
    # Define default configuration
    default_config = {
        "gitignore": {"respect": True},
        "output": {"size_limits": {"file_max_mb": 1.0}, "max_tokens": 10000},
    }

    try:
        config_path = config_dir / "smoosh.yaml"

        # If config file exists, load and merge with defaults
        if config_path.is_file():
            with open(config_path) as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    # Deep merge user config with defaults
                    return deep_merge(default_config, user_config)

        # If no config file or it's empty, return defaults
        return default_config

    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e


def deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries, updating base with values from update.

    Args:
        base: Base dictionary to merge into
        update: Dictionary with values to merge

    Returns:
        Merged dictionary
    """
    merged = base.copy()

    for key, value in update.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value

    return merged  # Added the missing return statement
