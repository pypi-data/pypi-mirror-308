from InquirerPy import inquirer
import click   
import time

from brwne_cli.gitEngine import GitEngine
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.utils.ANSI_Colors import *

@pre_command()
def branch_command(context: CommandContextData):
    curr_branch_type = RealtimeDBEngine().read_data(f"repo_branches/{context.repo_id}/{context.current_branch}/type")

    if curr_branch_type == "permanent":
        print(f"Current branch: {PURPLE}{BOLD}{context.current_branch} ({curr_branch_type}){RESET}")
    else:
        print(f"Current branch: {BLUE}{context.current_branch} ({curr_branch_type}){RESET}")
    
    # Determine the type of the new branch
    new_branch_type = "temporary"

    # If the current branch is permanent, prompt the user to choose the branch type
    if curr_branch_type == "permanent":
        options = ["temporary - Used to build and eventually merge onto a permanent branch", "permanent - long-term branches like `main`"]
        branch_type_choice = inquirer.select(
            message="Do you want to create a temporary or permanent branch?",
            choices=options,
        ).execute()
        selected_index = options.index(branch_type_choice)
        if selected_index == 0:
            new_branch_type = "temporary"
        else:
            new_branch_type = "permanent"
    
    if new_branch_type == "permanent":
        x = input(f"Name for this new permanent branch: {PURPLE}{BOLD}")
        # i wanna put the var branch_name in the buffer input, they can edit it and hit enter
        click.echo(RESET)
        new_branch_name = x
    else:
        x = input(f"Name for this new temporary branch: {BLUE}{BOLD}{context.current_branch}-")
        click.echo(RESET)
        new_branch_name = f"{context.current_branch}-{x.strip()}"
    
    # Check if the branch name is already taken
    branch_data = RealtimeDBEngine().read_data(f"repo_branches/{context.repo_id}/{new_branch_name}")
    if branch_data is not None:
        print(f"{RED}{BOLD}Error: Branch name {new_branch_name} already taken{RESET}")
        return
    
    # Step 4: Create the new branch
    GitEngine.create_switch_and_push_branch(new_branch_name)
    latest_commit_on_main_branch = GitEngine.get_latest_commit(f"origin/{new_branch_name}")
    RealtimeDBEngine().write_data(f"repo_branches/{context.repo_id}/{new_branch_name}", {
                            "parent": context.current_branch,
                            "type": new_branch_type,
                            "latest_pushed_commit": latest_commit_on_main_branch,
                            "created_at": int(time.time()),
                            "last_common_commit_to_parent": latest_commit_on_main_branch
                    })

    if new_branch_type == "permanent":
        print(f"You are now on {PURPLE}{BOLD}{new_branch_name}{RESET}")
    else:
        print(f"You are now on {BLUE}{BOLD}{new_branch_name}{RESET}")
    
