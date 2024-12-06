import click

from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.gitEngine import GitEngine
from brwne_cli.utils.ANSI_Colors import *

def all_zeros(arr):
    for i in arr:
        if i != 0:
            return False
    return True

def run_cascade(current_branch: str, branch_structure: dict):
    curr = current_branch
    path = []

    while curr != "":
        path.append(curr)
        curr = branch_structure[curr]["parent"]
        
    # check if we can pull the current branch
    GitEngine.fetch()

    path_unpulled_commits = [GitEngine.unpulled_commits_count_from_branch(branch_name=branch) for branch in path]

    for branch, comm_count in zip(path, path_unpulled_commits):
        print(f"{branch}: {comm_count}")
    
    if all_zeros(path_unpulled_commits):
        print("Cascade completed")
        return
    
    if path_unpulled_commits[0] == 0:
        # get the subset of the path till we reach the first place that had
        sub_path = [path[0]]
        for i in range(1,len(path)):
            sub_path.append(path[i])
            if path_unpulled_commits[i] != 0:
                break
        
        # work your way down the sub_path from the top to bottom updating files,
        # rebasing and pushing
        downward_sub_path = sub_path[::-1]
        for i in range(len(downward_sub_path)-1):
            upper = downward_sub_path[i]
            lower = downward_sub_path[i+1]

            should_push_lower_branch = i != len(downward_sub_path) - 2  # dont push the branch if its the current branch
            if GitEngine.rebase_down(branch_from=upper, branch_to=lower, push_lower_branch_after_rebase=should_push_lower_branch):
                click.echo(f"{GREEN}sucessfully rebased {upper} -> {lower}{RESET}")
                run_cascade(current_branch, branch_structure);
            else:
                click.echo(f"{RED}Error: Could not rebase {upper} -> {lower}{RESET}")
                click.echo(f"you are on {lower}, please run and fix conflicts {BLACK_BG_WHITE_TEXT}`git rebase origin/{upper}`{RESET}")
                return
    else:
        commits_to_pull_curr_branch = GitEngine.unpulled_commits_count_from_branch(branch_name=path[0])
        if commits_to_pull_curr_branch > 0:
            click.echo(f"There are {commits_to_pull_curr_branch} commits to pull from {path[0]}")
            # check if the rebase is possible
            was_able_to_rebase = GitEngine.attempt_rebase(branch_name=path[0])
            if not was_able_to_rebase:
                click.echo(f"Unable to rebase from origin/{path[0]} -> {current_branch} due to potential merge conflicts")
                click.echo(f"{RED}pls run {RESET}{BLACK_BG_WHITE_TEXT}`git rebase origin/{path[0]}`{RESET}")
            else:
                click.echo(f"{GREEN}sucessfully rebased origin/{path[0]} -> {current_branch}{RESET}")



@pre_command()
def cascade_command(context: CommandContextData):

    # this function stashes the current working changes and returns a function to unstash them
    unstash_func = GitEngine.stash_current_working_changes()

    if unstash_func is None:
        click.echo(f"{RED}Error: Could not stash current working changes{RESET}")
        return
    else:  
        # 0 means no changes to stash
        if unstash_func != 0:
            click.echo(f"{GREEN}Stashed current working changes{RESET}")

    branch_structure = RealtimeDBEngine().read_data(f"repo_branches/{context.repo_id}")
    
    # getting the path from the current branch to the root branch
    run_cascade(context.current_branch, branch_structure)                

    if unstash_func != 0:
        unstash_response = unstash_func()
        if unstash_response:
            click.echo(f"{GREEN}Unstashed working changes{RESET}")
        else:
            click.echo(f"{RED}Error: Could not unstash working changes{RESET}")
            return
    
