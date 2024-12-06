import click
import time
import subprocess

from brwne_cli.gitEngine import GitEngine
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.utils.ANSI_Colors import *

@pre_command()
def add_command(files, context: CommandContextData):
    """Start tracking changes for given files in the current branch."""
    # Check the type of our branch on the db (permanent or temporary)
    branch_type = RealtimeDBEngine().get_branch_type(context.repo_id, context.current_branch)

    if branch_type == "permanent":
        # You can't add files to a permanent branch
        # Create a new branch for the user

        current_branch_name = GitEngine.get_current_branch()
        click.echo(f"Currently on {PURPLE}{BOLD}{current_branch_name} (permanent){RESET}, You can't add files to a permanent branch.")
        click.echo(f"brwne will create a temporary branch from {current_branch_name} for you and add your files there.")
        x = input(f"Name for this new sub branch: {BLUE}{current_branch_name}-")
        click.echo(RESET)

        new_branch_name = f"{current_branch_name}-{x.strip()}"

        # TODO: Check if the branch already exists

        # Step 5A: Create the new branch (On Brwne & In git and add changes there)
        GitEngine.create_switch_and_push_branch(new_branch_name)

        # TODO: check if the branch was created successfully
        # TODO: check for if origin is always named 'origin'

        latest_commit_on_main_branch = GitEngine.get_latest_commit(f"origin/{new_branch_name}")
        RealtimeDBEngine().write_data(f"repo_branches/{context.repo_id}/{new_branch_name}", {
                            "parent": current_branch_name,
                            "type": "temporary",
                            "latest_pushed_commit": latest_commit_on_main_branch,
                            "created_at": int(time.time())
                    })
        
        # Step 6A: Add the files to the branch
        added_files_count = GitEngine.add_files(files)
        if added_files_count > 0:
            print(f"{BLUE}On branch {new_branch_name} (temporary), tracking {added_files_count} files currently.{RESET}")
        else:
            print(f"{RED}No untracked files to add!{RESET}")

    else:
        # Step 4B: Add the files to the branch
        added_files_count = GitEngine.add_files(files)
        if added_files_count > 0:
            print(f"{BLUE}On branch {context.current_branch}, tracking {added_files_count} files currently{RESET}")
        else:
            print(f"{RED}No untracked files to add!{RESET}")