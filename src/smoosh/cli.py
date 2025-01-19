"""Command line interface for smoosh."""

from time import sleep

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

console = Console()


def show_welcome() -> None:
    """Show welcome message."""
    console.print(
        Panel.fit(
            "🐍 [bold green]smoosh[/bold green] - Making Python packages digestible!",
            border_style="green",
        )
    )


@click.group()
@click.version_option()
def main() -> None:
    """Smoosh Python packages into digestible summaries."""
    show_welcome()


@main.command()
@click.argument("path", type=click.Path(exists=True))
def analyze(path: str) -> None:
    """Analyze a Python package."""
    console.print(f"🔍 Analyzing package at: [bold blue]{path}[/bold blue]")

    # Simulate analysis with progress bar
    for _ in track(range(5), description="Analyzing..."):
        sleep(0.2)

    console.print("✨ [bold green]Analysis complete![/bold green] (Coming soon...)")


@main.command()
@click.argument("path", type=click.Path(exists=True))
def summarize(path: str) -> None:
    """Generate LLM-friendly summary."""
    console.print(f"📝 Summarizing package at: [bold blue]{path}[/bold blue]")
    console.print("🚧 [yellow]Coming soon![/yellow]")


@main.command()
@click.argument("path", type=click.Path(exists=True))
def structure(path: str) -> None:
    """Show package structure."""
    console.print(f"📦 Analyzing structure of: [bold blue]{path}[/bold blue]")
    console.print("🚧 [yellow]Coming soon![/yellow]")


if __name__ == "__main__":
    main()
