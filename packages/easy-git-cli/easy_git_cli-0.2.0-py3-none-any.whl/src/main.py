#!/usr/bin/env python3
import os
import sys
import signal
import click
import questionary
from git import Repo, GitCommandError

aliases = {
    "c": "quick-commit",
    "h": "help",
}

class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if aliases.get(cmd_name) == x]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

def handle_kill_signal(signal_number, frame):
    """Handle kill signals like SIGINT and SIGTERM."""
    click.echo("\nReceived termination signal. Exiting gracefully...")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, handle_kill_signal)
signal.signal(signal.SIGTERM, handle_kill_signal)

@click.group(cls=AliasedGroup)
def cli():
    """easy-git: Simplify your Git workflows."""
    pass

def get_git_repo():
    """Return the current Git repository."""
    try:
        return Repo(os.getcwd())
    except:
        click.echo("Not a git repository.")
        sys.exit(1)


@cli.command()
def quick_commit():
    """Interactive add-commit cycle."""
    repo = get_git_repo()

    # Step 1: Get the list of changed files
    changed_files = [item.a_path for item in repo.index.diff(None)]  # Unstaged files
    changed_files += repo.untracked_files  # Untracked files

    if not changed_files:
        click.echo("No changes to commit!")
        return

    # Step 2: Select files using questionary's checkbox
    selected_files = questionary.checkbox(
        "Select files to stage (use 'a' to toggle all, 'j'/'k' to navigate):",
        choices=[{"name": file} for file in changed_files],
        validate=lambda answers: "You must select at least one file." if not answers else True,
        use_jk_keys=True,
        instruction="(space to select, 'a' to toggle all)"
    ).ask()

    if not selected_files:
        click.echo("No files selected.")
        return

    # Step 3: Add the selected files
    for file in selected_files:
        repo.git.add(file)
    click.echo("Files staged successfully!")

    # Step 4: Get commit message or amend
    commit_type = questionary.select(
        "Choose commit type:",
        choices=["New Commit", "Amend Last Commit"]
    ).ask()

    if commit_type == "New Commit":
        commit_message = click.prompt("Enter commit message")
        repo.git.commit(m=commit_message)
    elif commit_type == "Amend Last Commit":
        repo.git.commit("--amend", "--no-edit")
        click.echo("Amended the last commit.")

    # Step 5: Push changes
    push_choice = questionary.confirm("Would you like to push now?", auto_enter=False).ask()
    if push_choice:
        try:
            repo.git.push()
            click.echo("Pushed to the remote repository.")
        except GitCommandError:
            click.echo("Error: Unable to push. Check your remote settings.")
    else:
        click.echo("Skipped pushing.")

if __name__ == "__main__":
    cli()
