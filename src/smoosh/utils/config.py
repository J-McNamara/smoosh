"""Configuration handling for smoosh."""

import os
from pathlib import Path
from typing import Any, Dict, TypedDict, Union, cast

import yaml

# Define PathLike type consistently with other modules
PathLike = Union[str, "os.PathLike[str]"]


class SizeLimitsDict(TypedDict):
    file_max_mb: float


class OutputDict(TypedDict):
    max_tokens: int
    size_limits: SizeLimitsDict


class ThresholdsDict(TypedDict):
    cat_threshold: int
    fold_threshold: int


class GitignoreDict(TypedDict):
    respect: bool


class ConfigDict(TypedDict):
    output: OutputDict
    thresholds: ThresholdsDict
    gitignore: GitignoreDict


DEFAULT_CONFIG: ConfigDict = {
    "output": {"max_tokens": 5000, "size_limits": {"file_max_mb": 1.0}},
    "thresholds": {"cat_threshold": 5000, "fold_threshold": 15000},
    "gitignore": {"respect": True},
}


def load_config(repo_path: PathLike) -> ConfigDict:
    """Load configuration from repo_path/smoosh.yaml or use defaults.

    Args:
    ----
        repo_path: Path to the repository root

    Returns:
    -------
        Dict containing merged configuration (defaults + user config)

    Raises:
    ------
        ConfigurationError: If config file exists but is invalid

    """
    repo_path = Path(str(repo_path))
    config_path = repo_path / "smoosh.yaml"

    # Start with default configuration
    config = cast(ConfigDict, DEFAULT_CONFIG.copy())

    # If config file exists, load and merge it
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    config = deep_merge(config, user_config)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in config file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading config file: {e}")

    # Validate the final configuration
    validate_config(config)
    return config


def validate_config(config: ConfigDict) -> None:
    """Validate configuration values.

    Args:
    ----
        config: Configuration dictionary to validate

    Raises:
    ------
        ConfigurationError: If configuration is invalid

    """
    # Check required sections
    required_sections = ["output", "thresholds", "gitignore"]
    for section in required_sections:
        if section not in config:
            raise ConfigurationError(f"Missing required config section: {section}")

    # Validate output section
    output = config["output"]
    if not isinstance(output.get("max_tokens"), int) or output["max_tokens"] <= 0:
        raise ConfigurationError("output.max_tokens must be a positive integer")

    size_limits = output.get("size_limits", {})
    if (
        not isinstance(size_limits.get("file_max_mb"), (int, float))
        or size_limits["file_max_mb"] <= 0
    ):
        raise ConfigurationError("output.size_limits.file_max_mb must be a positive number")

    # Validate thresholds
    thresholds = config["thresholds"]
    if not isinstance(thresholds.get("cat_threshold"), int) or thresholds["cat_threshold"] <= 0:
        raise ConfigurationError("thresholds.cat_threshold must be a positive integer")
    if not isinstance(thresholds.get("fold_threshold"), int) or thresholds["fold_threshold"] <= 0:
        raise ConfigurationError("thresholds.fold_threshold must be a positive integer")
    if thresholds["cat_threshold"] >= thresholds["fold_threshold"]:
        raise ConfigurationError("cat_threshold must be less than fold_threshold")


def deep_merge(base: ConfigDict, update: Dict[str, Any]) -> ConfigDict:
    """Recursively merge two dictionaries.

    Args:
    ----
        base: Base dictionary
        update: Dictionary to merge into base

    Returns:
    -------
        Merged dictionary

    """
    merged = base.copy()
    valid_keys = {"output", "thresholds", "gitignore"}

    for key, value in update.items():
        if key not in valid_keys:
            continue

        if key == "output" and isinstance(value, dict):
            if isinstance(merged["output"], dict):
                output_dict = merged["output"].copy()
                if "max_tokens" in value:
                    output_dict["max_tokens"] = value["max_tokens"]
                if "size_limits" in value and isinstance(value["size_limits"], dict):
                    size_limits = output_dict["size_limits"].copy()
                    if "file_max_mb" in value["size_limits"]:
                        size_limits["file_max_mb"] = value["size_limits"]["file_max_mb"]
                    output_dict["size_limits"] = size_limits
                merged["output"] = cast(OutputDict, output_dict)

        elif key == "thresholds" and isinstance(value, dict):
            if isinstance(merged["thresholds"], dict):
                thresholds_dict = merged["thresholds"].copy()
                if "cat_threshold" in value:
                    thresholds_dict["cat_threshold"] = value["cat_threshold"]
                if "fold_threshold" in value:
                    thresholds_dict["fold_threshold"] = value["fold_threshold"]
                merged["thresholds"] = cast(ThresholdsDict, thresholds_dict)

        elif key == "gitignore" and isinstance(value, dict):
            if isinstance(merged["gitignore"], dict):
                gitignore_dict = merged["gitignore"].copy()
                if "respect" in value:
                    gitignore_dict["respect"] = value["respect"]
                merged["gitignore"] = cast(GitignoreDict, gitignore_dict)

    return merged


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

    pass
