"""Command line interface for smoosh."""

from pathlib import Path
from typing import Any, Dict, Optional, cast

import click
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import AnalysisError, ConfigurationError, GenerationError, __version__
from .analyzer.repository import analyze_repository
from .composer.concatenator import concatenate_files
from .utils.config import ConfigDict, load_config

console = Console()


def show_welcome() -> None:
    """Show welcome message with version."""
    console.print(
        Panel.fit(
            "🐍 [bold green]smoosh v{__version__}[/bold green] - "
            "Making Python packages digestible!",
            border_style="green",
        )
    )


def show_stats(stats: Dict[str, Any]) -> None:
    """Display analysis and generation statistics."""
    table = Table(title="Analysis Results", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    for key, value in stats.items():
        table.add_row(key, str(value))
    console.print(table)


@click.command()
@click.argument(
    "target",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.option(
    "--mode",
    type=click.Choice(["cat", "fold", "smoosh"]),
    default="cat",
    help="Compression mode (cat: full concatenation, fold/smoosh: coming soon)",
)
@click.option("--output", "-o", type=str, help="Output file path")
@click.option("--force-cat", is_flag=True, help="Override gitignore and size limits")
@click.version_option(version=__version__)
def main(target: str, mode: str, output: Optional[str], force_cat: bool) -> None:
    """Smoosh software packages into plaintext summaries on the clipboard.

    TARGET can be a code repository, directory of text files, or a text file.
    """
    show_welcome()

    try:
        # Convert paths
        target_path = Path(target)
        output_path = Path(output) if output else None

        # Load configuration, looking for smoosh.yaml in the directory
        config_dir = target_path if target_path.is_dir() else target_path.parent
        config = cast(ConfigDict, load_config(config_dir))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Analyze repository
            progress.add_task("Analyzing repository...", total=None)
            repo_info = analyze_repository(target_path, config, force_cat)

            # Compose output
            progress.add_task("Generating summary...", total=None)
            result, stats = concatenate_files(repo_info, mode, config)

            # Handle output
            if output_path:
                output_path.write_text(result)
                console.print(f"✨ Output written to: [bold blue]{output_path}[/bold blue]")
            else:
                pyperclip.copy(result)
                console.print("✨ Output copied to clipboard!")

            # Show statistics
            show_stats(stats)

    except (ConfigurationError, AnalysisError, GenerationError) as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        raise click.Abort() from e
    except Exception as e:
        console.print("[bold red]An unexpected error occurred![/bold bold]")
        console.print(f"[red]{e!s}[/red]")
        raise click.Abort() from e


if __name__ == "__main__":
    main()
