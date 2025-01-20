"""Command line interface for smoosh."""

from pathlib import Path
from typing import Any, Dict, Optional

import click
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import AnalysisError, ConfigurationError, GenerationError, __version__
from .analyzer.repository import analyze_repository
from .composer.concatenator import concatenate_files
from .utils import load_config, resolve_path

console = Console()


def show_welcome() -> None:
    """Show welcome message with version."""
    console.print(
        Panel.fit(
            f"\U0001f40d [bold green]smoosh v{__version__}[/bold green] - "
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


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("path")
@click.option(
    "--mode",
    type=click.Choice(["cat", "fold", "smoosh"]),
    default="cat",
    help="Processing mode (default: cat)",
)
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--force-cat", is_flag=True, help="Override gitignore and size limits")
@click.version_option(version=__version__)
def main(path: str, mode: str, output: Optional[str], force_cat: bool) -> None:
    """Smoosh Python packages into digestible summaries.

    PATH can be either a filesystem path or an installed package name.
    """
    show_welcome()

    try:
        # Resolve path or package name
        target_path = resolve_path(path)
        output_path = Path(output) if output else None

        if not target_path.is_dir():
            console.print(f"[bold red]Error:[/bold red] {path} is not a directory")
            raise click.Abort()

        console.print(f"Processing: [bold blue]{target_path}[/bold blue]")

        # Load config and process
        process_directory(target_path, mode, output_path, force_cat)

    except FileNotFoundError as err:
        console.print(f"[bold red]Error:[/bold red] {str(err)}")
        raise click.Abort() from err
    except Exception as err:
        console.print(f"[bold red]Error:[/bold red] An unexpected error occurred: {str(err)}")
        raise click.Abort() from err


def process_directory(path: Path, mode: str, output: Optional[Path], force_cat: bool) -> None:
    """Process a directory with the specified mode."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Analyze repository
            progress.add_task("Analyzing...", total=None)
            repo_info = analyze_repository(path, load_config(path), force_cat)

            # Compose output
            progress.add_task("Generating summary...", total=None)
            result, stats = concatenate_files(repo_info, mode, load_config(path))

            # Handle output
            if output:
                output.write_text(result)
                console.print(f"\u2728 Output written to: [bold blue]{output}[/bold blue]")
            else:
                pyperclip.copy(result)
                console.print("\u2728 Output copied to clipboard!")

            # Show statistics
            show_stats(stats)

    except (ConfigurationError, AnalysisError, GenerationError) as err:
        console.print(f"[bold red]Error:[/bold red] {str(err)}")
        raise click.Abort() from err
    except Exception as err:
        console.print("[bold red]An unexpected error occurred![/bold red]")
        console.print(f"[red]{str(err)}[/red]")
        raise click.Abort() from err


if __name__ == "__main__":
    main()
