#!/usr/bin/env python3
"""
Lucida Flow CLI
Command-line interface for downloading music from Lucida.to
"""

import click
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from lucida_client import LucidaClient

# Load environment variables
load_dotenv()

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Lucida Flow - Download music from various streaming services via Lucida.to"""
    pass


@cli.command()
@click.argument("query")
@click.option(
    "--service",
    "-s",
    default="amazon_music",
    type=click.Choice(
        [
            "amazon_music",
            "tidal",
            "qobuz",
            "spotify",
            "deezer",
            "soundcloud",
            "yandex_music",
        ],
        case_sensitive=False,
    ),
    help="Music service to search (default: amazon_music)",
)
@click.option("--limit", "-l", default=10, help="Maximum number of results")
def search(query, service, limit):
    """Search for music on a specific service"""
    console.print(f"\n[bold cyan]Searching {service} for:[/bold cyan] {query}\n")

    with console.status("[bold green]Searching..."):
        client = LucidaClient()
        results = client.search(query, service=service, limit=limit)

    if "error" in results:
        console.print(f"[bold red]Error:[/bold red] {results['error']}")
        return

    tracks = results.get("tracks", [])

    if not tracks:
        console.print("[yellow]No results found[/yellow]")
        return

    # Create table
    table = Table(title=f"Search Results ({len(tracks)} tracks)")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Title", style="green")
    table.add_column("Artist", style="yellow")
    table.add_column("Album", style="magenta")

    for idx, track in enumerate(tracks, 1):
        table.add_row(
            str(idx),
            track.get("name", "Unknown"),
            track.get("artist", "Unknown"),
            track.get("album", "Unknown"),
        )

    console.print(table)
    console.print()


@cli.command()
@click.argument("url")
@click.option("--output", "-o", help="Output directory", default=None)
def download(url, output):
    """Download a track from URL"""
    console.print(f"\n[bold cyan]Downloading from:[/bold cyan] {url}\n")

    with console.status("[bold green]Preparing download..."):
        client = LucidaClient()

        # Get track info first
        info = client.get_track_info(url)

        if "error" in info:
            console.print(
                f"[bold red]Error getting track info:[/bold red] {info['error']}"
            )
        elif info.get("name"):
            console.print(f"[bold]Track:[/bold] {info['name']}")
            if info.get("artist"):
                console.print(f"[bold]Artist:[/bold] {info['artist']}")
            if info.get("album"):
                console.print(f"[bold]Album:[/bold] {info['album']}")
            console.print()

    with console.status("[bold green]Downloading..."):
        result = client.download_track(url, output)

    if result.get("success"):
        console.print(f"[bold green]✓ Download successful![/bold green]")
        console.print(f"[bold]Saved to:[/bold] {result['filepath']}")
        console.print(
            f"[bold]Size:[/bold] {result['size']:,} bytes ({result['size'] / 1024 / 1024:.2f} MB)"
        )
    else:
        console.print(
            f"[bold red]✗ Download failed:[/bold red] {result.get('error', 'Unknown error')}"
        )


@cli.command()
@click.argument("url")
def info(url):
    """Get information about a track"""
    console.print(f"\n[bold cyan]Getting info for:[/bold cyan] {url}\n")

    with console.status("[bold green]Fetching information..."):
        client = LucidaClient()
        track_info = client.get_track_info(url)

    if "error" in track_info:
        console.print(f"[bold red]Error:[/bold red] {track_info['error']}")
        return

    # Display track information
    table = Table(title="Track Information")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    for key, value in track_info.items():
        if value and key != "error":
            table.add_row(key.capitalize(), str(value))

    console.print(table)
    console.print()


@cli.command()
def services():
    """List available streaming services"""
    console.print("\n[bold cyan]Available Services:[/bold cyan]\n")

    client = LucidaClient()
    services_list = client.get_available_services()

    for service in services_list:
        console.print(f"  [green]✓[/green] {service}")

    console.print(f"\n[dim]Total: {len(services_list)} services[/dim]\n")


@cli.command()
def config():
    """Show current configuration"""
    console.print("\n[bold cyan]Current Configuration:[/bold cyan]\n")

    table = Table()
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    base_url = os.getenv("LUCIDA_BASE_URL", "https://lucida.to")
    download_dir = os.getenv("DOWNLOAD_DIR", "./downloads")
    timeout = os.getenv("REQUEST_TIMEOUT", "30")

    table.add_row("Base URL", base_url)
    table.add_row("Download Directory", download_dir)
    table.add_row("Request Timeout", f"{timeout}s")

    console.print(table)
    console.print()


if __name__ == "__main__":
    cli()
