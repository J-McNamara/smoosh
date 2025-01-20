"""Configuration handling for smoosh."""

import os
from typing import Any, Dict, TypedDict, Union, cast

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


def deep_merge(base: ConfigDict, update: Dict[str, Any]) -> ConfigDict:
    """Recursively merge two dictionaries.

    Args:
    ----
        base: Base dictionary.
        update: Dictionary to merge into base.

    Returns:
    -------
        Merged dictionary.

    """
    merged = base.copy()
    valid_keys = {"output", "thresholds", "gitignore"}

    for key, value in update.items():
        if key not in valid_keys or not isinstance(value, dict):
            continue

        if key == "output" and isinstance(merged["output"], dict):
            merged["output"] = cast(OutputDict, _merge_output(merged["output"], value))
        elif key == "thresholds" and isinstance(merged["thresholds"], dict):
            merged["thresholds"] = cast(
                ThresholdsDict, _merge_thresholds(merged["thresholds"], value)
            )
        elif key == "gitignore" and isinstance(merged["gitignore"], dict):
            merged["gitignore"] = cast(GitignoreDict, _merge_gitignore(merged["gitignore"], value))

    return merged


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

    pass


def load_config(config_path: Union[PathLike, None] = None) -> ConfigDict:
    """Load configuration from file.

    Args:
    ----
        config_path: Path to configuration file. If None, returns default config.

    Returns:
    -------
        Loaded configuration dictionary.

    Raises:
    ------
        ConfigurationError: If configuration is invalid.
    """
    if config_path is None:
        return DEFAULT_CONFIG.copy()

    try:
        import yaml

        with open(config_path) as f:
            user_config = yaml.safe_load(f)
        if not isinstance(user_config, dict):
            raise ConfigurationError("Configuration must be a dictionary")
        return deep_merge(DEFAULT_CONFIG, user_config)
    except Exception as err:
        raise ConfigurationError(f"Failed to load configuration: {err!s}") from err
