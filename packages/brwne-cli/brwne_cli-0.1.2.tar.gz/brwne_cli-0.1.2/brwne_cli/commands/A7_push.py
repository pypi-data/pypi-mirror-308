import click

from brwne_cli.gitEngine import GitEngine
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.utils.ANSI_Colors import *

@pre_command()
def push_command(context: CommandContextData):

    # get the list of commits to push to this branch
    commits_generator = GitEngine.get_commits_to_push()
    if not commits_generator:
        click.echo(f"{RED}No commits to push{RESET}")
        return
    
    print(f"Commits to push: {commits_generator}")
    # NOTE: commits is a generator
    commit_hashes = []
    for com in commits_generator:
        commit_hashes.append(com)

    
    if GitEngine.push_commits():
        click.echo(f"{BLUE}Pushed commits successfully{RESET}")
    else:
        click.echo(f"{RED}There was an error while attempting to push commits{RESET}")
        return

    # Get the latest pushed commit on a branch
    latest_commit_on_main_branch = GitEngine.get_latest_commit(context.current_branch)
    RealtimeDBEngine().write_data(f"repo_branches/{context.repo_id}/{context.current_branch}/latest_pushed_commit", latest_commit_on_main_branch)

    # delete the unpushed diff data from the database
    for com in commit_hashes:
        click.echo(f"Deleting diff data for {com}")
        RealtimeDBEngine().delete_data(f"branch_diffs/{context.repo_id}/{context.current_branch}/unpushed_diffs/{com}")
    
    click.echo(f"Latest pushed commit on {context.current_branch}: {latest_commit_on_main_branch}")
    

