"""Configuration management utilities."""
from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        return yaml.safe_load(f)


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration structure."""
    required_keys = {"api", "processing", "storage"}
    return all(key in config for key in required_keys)
