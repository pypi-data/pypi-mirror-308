from pathlib import Path

import copier
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="components",
    help="Install and update components from basic-components",
    add_completion=False,
)

console = Console()

# Default values for REPO_URL and COMPONENTS_DIR
DEFAULT_REPO_URL = "https://github.com/basicmachines-co/basic-components.git"
DEFAULT_COMPONENTS_DIR = Path("components/ui")
DEFAULT_BRANCH = "main"

# typer cli arg options
COMPONENTS_DIR_OPTION = typer.Option(DEFAULT_COMPONENTS_DIR, "--components-dir", "-d", help="Directory to update components in")
REPO_URL_OPTION = typer.Option(DEFAULT_REPO_URL, "--repo-url", "-r", help="Repository URL to update from")
BRANCH_OPTION = typer.Option(DEFAULT_BRANCH, "--branch", "-b", help="Branch, tag, or commit to update from")


def add_component(
    component: str,
    dest_dir: Path,
    repo_url: str = DEFAULT_REPO_URL,
    branch: str = DEFAULT_BRANCH,
) -> None:
    """Add a specific component to the project."""
    try:
        console.print(f"[green]Installing {component} from '{repo_url}' ...[/green]")

        copier.run_copy(
            src_path=repo_url,
            dst_path=str(dest_dir),
            exclude=[
                "*",
                f"!{component}",
            ],
            vcs_ref=branch,
        )

    except Exception as e:  # pyright: ignore [reportAttributeAccessIssue]
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def add(
    component: str = typer.Argument(..., help="Name of the component to install"),
    branch: str = typer.Option(
        DEFAULT_BRANCH, "--branch", "-b", help="Branch, tag, or commit to install from"
    ),
    repo_url: str = typer.Option(
        DEFAULT_REPO_URL, "--repo-url", "-r", help="Repository URL to use"
    ),
    components_dir: Path = typer.Option(
        DEFAULT_COMPONENTS_DIR, "--components-dir", "-d", help="Directory to install components"
    )
) -> None:
    """Add a component to your project."""
    try:
        add_component(component, components_dir, repo_url, branch)

        console.print(
            Panel(
                f"[green]✓[/green] Added {component} component\n\n"
                f"[cyan] components-dir={components_dir}[/cyan]",
                title="Installation Complete",
                border_style="green",
            )
        )
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def init(
    components_dir: Path = COMPONENTS_DIR_OPTION,
) -> None:
    """Initialize project for basic-components."""
    # Create components directory structure
    components_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        Panel(
            "[green]✓[/green] Initialized basic-components\n\n"
            "Directory structure created:\n"
            f"   [cyan]{components_dir}[/cyan]\n\n"
            "Next steps:\n\n"
            "1. Add the cn() utility function:\n"
            "   [cyan]components.basicmachines.co/docs/utilities#cn[/cyan]\n\n"
            "2. Configure JinjaX to use the components directory:\n"
            "   [cyan]components.basicmachines.co/docs/utilities#jinjax[/cyan]\n\n"
            "3. Start adding components:\n"
            "   [cyan]components add button[/cyan]\n\n"
            "View all available components:\n"
            "   [cyan]components.basicmachines.co/docs/components[/cyan]",
            title="Setup Complete",
            border_style="green",
        )
    )


if __name__ == "__main__":
    app()