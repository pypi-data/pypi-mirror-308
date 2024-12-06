import click

from brwne_cli.gitEngine import GitEngine
from brwne_cli.utils.ANSI_Colors import *
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.fireEngine import RealtimeDBEngine

@pre_command()
def switch_command(branch_name: str, context: CommandContextData):
    if GitEngine.switch_to_branch(branch_name):
        branch_type = RealtimeDBEngine().get_branch_type(context.repo_id, branch_name)
        if branch_type == "permanent":
            click.echo(f"{BOLD}Switched to branch {PURPLE}{branch_name} ({branch_type}){RESET}")
        else:
            click.echo(f"{BOLD}Switched to branch {BLUE}{branch_name} ({branch_type}){RESET}")
    else:
        click.echo(f"{RED}{BOLD}Error: Could not switch to branch {branch_name}{RESET}")