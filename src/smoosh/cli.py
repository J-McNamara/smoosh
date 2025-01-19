"""Command line interface for smoosh."""

from pathlib import Path
from typing import Optional

import click
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import AnalysisError, ConfigurationError, GenerationError, __version__
from .analyzer.repository import analyze_repository
from .composer.concatenator import concatenate_files
from .utils import load_config, resolve_path  # Updated import

console = Console()


def show_welcome():
    """Show welcome message with version."""
    console.print(
        Panel.fit(
            f"🐍 [bold green]smoosh v{__version__}[/bold green] - Making Python packages digestible!",
            border_style="green",
        )
    )


def show_stats(stats: dict):
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
def main(path: str, mode: str, output: Optional[str], force_cat: bool):
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
        config = load_config(target_path)
        process_directory(target_path, mode, output_path, force_cat)

    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] An unexpected error occurred: {str(e)}")
        raise click.Abort()


def process_directory(path: Path, mode: str, output: Optional[Path], force_cat: bool):
    """Process a directory with the specified mode."""
    try:
        # Load configuration
        config = load_config(path)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Analyze repository
            progress.add_task("Analyzing...", total=None)
            repo_info = analyze_repository(path, config, force_cat)

            # Compose output
            progress.add_task("Generating summary...", total=None)
            result, stats = concatenate_files(repo_info, mode, config)

            # Handle output
            if output:
                output.write_text(result)
                console.print(f"✨ Output written to: [bold blue]{output}[/bold blue]")
            else:
                pyperclip.copy(result)
                console.print("✨ Output copied to clipboard!")

            # Show statistics
            show_stats(stats)

    except (ConfigurationError, AnalysisError, GenerationError) as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()
    except Exception as e:
        console.print("[bold red]An unexpected error occurred![/bold red]")
        console.print(f"[red]{str(e)}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    main()
