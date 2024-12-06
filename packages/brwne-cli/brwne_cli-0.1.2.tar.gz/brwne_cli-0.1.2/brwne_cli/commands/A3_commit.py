import click
import time

from brwne_cli.gitEngine import GitEngine
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.utils.ANSI_Colors import *

# TODO: check if the user is on a perment branch, if so, create a temp branch for them, move thier tracked changes there and aid them to make a commit there

@pre_command(request_UID=True)
def commit_command(message: str, context: CommandContextData):

    commit_response = GitEngine.commit_changes(message)

    if commit_response is None:
        print(f"{RED}{BOLD}Error: Could not commit changes{RESET}")
        return
    elif commit_response == -1:
        print(f"{RED}{BOLD}Unable to commit as brwne is not tracking any files, (use `br add` to track changes){RESET}")
        return
    else:
        print(f"{BLUE}Commit successful - {commit_response[:7]}{RESET}")

    # Step 5: Get the diff between the latest pushed commit and the current commit
    latest_commit_on_main_branch = RealtimeDBEngine().read_data(f"repo_branches/{context.repo_id}/{context.current_branch}/latest_pushed_commit")
    diff = GitEngine.get_diff_between_commits(latest_commit_on_main_branch, commit_response)

    # Step 6: Get the parent commit of the current commit
    parent_commit = GitEngine.get_parent_commit(commit_response)

    # Step 7: Save the diff to the database
    RealtimeDBEngine().write_data(f"branch_diffs/{context.repo_id}/{context.current_branch}/unpushed_diffs/{commit_response}", {
        "author": context.uid,
        "diff": diff,
        "parent_commit": parent_commit,
        "created_at": int(time.time())
    })

    # Step 8: Remove old diff data if it has the same hash as the parent commit
    RealtimeDBEngine().delete_data(f"branch_diffs/{context.repo_id}/{context.current_branch}/unpushed_diffs/{parent_commit}")