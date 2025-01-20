"""Format composition outputs in various styles."""

import json
from typing import Any, Dict

import yaml

from .. import GenerationError


class FormattingError(GenerationError):
    """Raised when formatting fails."""

    pass


def format_output(content: str, stats: Dict[str, Any], format_type: str = "text") -> str:
    """Format the composed content in the specified style.

    Args:
    ----
        content: Composed content
        stats: Composition statistics
        format_type: Output format style ('text', 'json', 'yaml', 'markdown')

    Returns:
    -------
        Formatted composition

    Raises:
    ------
        FormattingError: If formatting fails

    """
    try:
        formatters = {
            "text": format_text,
            "json": format_json,
            "yaml": format_yaml,
            "markdown": format_markdown,
        }

        if format_type not in formatters:
            raise FormattingError(f"Unknown format type: {format_type}")

        return formatters[format_type](content, stats)
    except Exception as e:
        raise FormattingError(f"Failed to format composition: {e}") from e


def format_text(content: str, stats: Dict[str, Any]) -> str:
    """Format composition as plain text.

    Args:
    ----
        content: Composed content
        stats: Composition statistics

    Returns:
    -------
        Formatted text

    """
    stats_section = "Composition Statistics:\n" + "\n".join(
        f"{key}: {value}" for key, value in stats.items()
    )

    return f"{stats_section}\n\n{content}"


def format_json(content: str, stats: Dict[str, Any]) -> str:
    """Format composition as JSON.

    Args:
    ----
        content: Composed content
        stats: Composition statistics

    Returns:
    -------
        JSON string

    """
    data = {"statistics": stats, "composition": content}
    return json.dumps(data, indent=2)


def format_yaml(content: str, stats: Dict[str, Any]) -> str:
    """Format composition as YAML.

    Args:
    ----
        content: Composed content
        stats: Composition statistics

    Returns:
    -------
        YAML string

    """
    data = {"statistics": stats, "composition": content}
    return yaml.dump(data, sort_keys=False)


def format_markdown(content: str, stats: Dict[str, Any]) -> str:
    """Format composition as Markdown.

    Args:
    ----
        content: Composed content
        stats: Composition statistics

    Returns:
    -------
        Markdown string

    """
    # Create statistics table
    stats_table = [
        "| Metric | Value |",
        "|--------|-------|",
    ]
    stats_table.extend(f"| {key} | {value} |" for key, value in stats.items())

    sections = [
        "# Repository Composition",
        "",
        "## Statistics",
        "",
        "\n".join(stats_table),
        "",
        "## Content",
        "",
        "```",
        content,
        "```",
    ]

    return "\n".join(sections)
