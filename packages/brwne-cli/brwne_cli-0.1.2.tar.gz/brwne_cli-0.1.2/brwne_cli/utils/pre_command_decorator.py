import click
from pydantic import BaseModel
from typing import Optional

from brwne_cli.gitEngine import GitEngine
from brwne_cli.utils.get_repoID_from_local import get_repo_id
from brwne_cli.fireEngine import RealtimeDBEngine

RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0;0m"

class CommandContextData(BaseModel):
    repo_id: Optional[str] = None
    unpushed_commit_count: Optional[int] = None
    current_branch: Optional[str] = None
    uid: Optional[str] = None   # TODO: deal with the fact this can be null if no network connection

def pre_command(supress_unpushed_commits_message=False, request_UID=False):
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            this_commands_context = CommandContextData()

            # getting the repo_id
            repo_id = get_repo_id()
            if not repo_id:
                print(f"{RED}{BOLD}Error: Could not find the repository ID. Are you sure you're inside a brwne repository?{RESET}")
                return
            this_commands_context.repo_id = repo_id  # setting the repo_id

            # getting the number of unpushed commits
            if not supress_unpushed_commits_message:
                unpushed_commit_count = GitEngine.count_unpushed_commits()
            else:
                unpushed_commit_count = None

            this_commands_context.unpushed_commit_count = unpushed_commit_count  # setting the unpushed_commit_count

            # getting the current branch
            this_commands_context.current_branch = GitEngine.get_current_branch()

            if request_UID:
                if uid := RealtimeDBEngine().get_UID():
                    this_commands_context.uid = uid
                else:
                    print(f"{RED}{BOLD}Error: Could not get the UID (){RESET}")

            # Pass the context to the function
            kwargs["context"] = this_commands_context
            return func(*args, **kwargs)
        return wrapper
    
    return decorator
