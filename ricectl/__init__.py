#!/opt/rice/env/bin/python3
# Name: ricectl.py
# Description: Control rice setup, installation, and upgrading
# Usage: ricectl.py command [options...]
# Author: Caleb Stewart <caleb.stewart94@gmail.com>
import json
import subprocess

import typer
from git.repo import Repo
from git.remote import FetchInfo
from rich.console import Console
from rich.progress import Progress

from ricectl.config import Config

# Root typer application
root = typer.Typer(help="Manage RICE installation, update and synchronization")
config_app = typer.Typer(help="Manage configuration")
root.add_typer(config_app)

# Load configuration
config = Config()

# Create a global console instance
console = Console(log_path=False)


@root.command("sync")
def rice_sync():
    """Synchronize the RICE repository with remote"""

    # Load the repository
    repo = Repo(config.repo)

    infos = repo.remotes.origin.fetch()
    for info in infos:
        if (info.flags & FetchInfo.HEAD_UPTODATE) != 0:
            break
    else:
        console.log(
            f"Already up-to-date on {repo.active_branch.name}@{repo.active_branch.commit.hexsha[:7]} ({repo.active_branch.commit.summary})"
        )
        return

    with Progress(console=console, transient=True, expand=True) as progress:

        task = progress.add_task("Updating")

        def update_progress(op_code, cur_count, max_count=None, message=""):
            if max_count is not None:
                progress.update(task, total=max_count)

            if message != "":
                progress.update(
                    task, completed=cur_count, description=f"Updating: {message}"
                )
            else:
                progress.update(task, completed=cur_count)

        repo.remotes.origin.pull(progress=update_progress)


@root.command("apply")
def rice_apply():
    """Apply the current state of the RICE using Ansible"""


@root.command("update")
def rice_update():
    """Synchronize the RICE repository and then apply the updated state with Ansible if there were changes."""

    # Sync the repository
    rice_sync()

    # Apply any changes
    rice_apply()


@root.command("status")
def rice_status():
    """Retrieve the current state of the RICE repository"""


@root.command("help")
def rice_help():
    """Print detailed documentation/help information"""


@config_app.command("set")
def config_set(param: str, value: str):
    """Set a value in the RICE configuration. The parameter name
    must exist in the configuration, and the value will be parsed
    into the requisite type. If the value is not valid, nothing is
    changed."""


if __name__ == "__main__":
    root()
