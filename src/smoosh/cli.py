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
from .utils.config import load_config

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


@click.group()
@click.version_option(version=__version__)
def main():
    """Smoosh Python packages into digestible summaries."""
    show_welcome()


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--mode",
    type=click.Choice(["cat", "fold", "smoosh"]),
    default="cat",
    help="Compression mode (cat: full concatenation, fold/smoosh: coming soon)",
)
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--force-cat", is_flag=True, help="Override gitignore and size limits")
def process(path: str, mode: str, output: Optional[str], force_cat: bool):
    """Process a Python package with the specified mode."""
    path = Path(path)
    output_path = Path(output) if output else None

    try:
        # Load configuration
        config = load_config(path)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Analyze repository
            progress.add_task("Analyzing repository...", total=None)
            repo_info = analyze_repository(path, config, force_cat)

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
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()
    except Exception as e:
        console.print("[bold red]An unexpected error occurred![/bold red]")
        console.print(f"[red]{str(e)}[/red]")
        raise click.Abort()


@main.command()
@click.argument("path", type=click.Path(exists=True))
def structure(path: str):
    """Show package structure without processing."""
    try:
        config = load_config(Path(path))
        repo_info = analyze_repository(Path(path), config, force_cat=False)
        console.print(repo_info.get_tree_representation())
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()


if __name__ == "__main__":
    main()
