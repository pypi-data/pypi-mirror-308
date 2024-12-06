from brwne_cli.gitEngine import GitEngine
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.utils.ANSI_Colors import *

@pre_command()
def status_command(context: CommandContextData):
    
    curr_branch_type = RealtimeDBEngine().get_branch_type(context.repo_id, context.current_branch)

    if curr_branch_type == "permanent":
        statement = f"Currently on: {PURPLE}{BOLD}{context.current_branch} ({curr_branch_type}){RESET}"
        if context.unpushed_commit_count > 0:
            statement += f" [{context.unpushed_commit_count} unpushed commits]"
        print(statement)
    else:
        statement = f"Currently on: {BLUE}{context.current_branch} ({curr_branch_type}){RESET}"
        if context.unpushed_commit_count > 0:
            statement += f" [{context.unpushed_commit_count} unpushed commits]"
        print(statement)

    if status:= GitEngine.get_status():
        print(status)

        if curr_branch_type == "permanent":
            print(f"{BOLD} ⚠️ {RESET}{PURPLE}Your on a permanent branch {BOLD}{context.current_branch} ({curr_branch_type}){RESET}{PURPLE}, create a temprory branch to make changes `br branch`{RESET}")
    else:
        print("⚠️ Error: Unable to retrieve git status.")