import os
import re
import click
import time

from brwne_cli.commands.auth import user_is_logged_in
from brwne_cli.utils.ANSI_Colors import *
from brwne_cli.gitEngine import GitEngine  # Assuming this is the Git engine class you created
from brwne_cli.fireEngine import RealtimeDBEngine  
from brwne_cli.utils.get_repoID_from_local import get_repo_id 


# Updated function to handle edge cases
def get_repo_folder_name(repo_url: str) -> str:
    """
    Extract the folder name from a repository URL.

    Args:
        repo_url (str): The repository URL (e.g., 'https://github.com/user/repo.git').

    Returns:
        str: The name of the folder that the repository will be cloned into.
    """
    # Remove trailing ".git" and any trailing slashes
    repo_name = re.sub(r"\.git/?$", "", repo_url)

    # Extract the last segment after the last "/"
    repo_name = repo_name.rstrip("/").split("/")[-1]

    return repo_name

def clone_command(repo_url: str):
    # Step 1: Check if user is logged in
    if not user_is_logged_in():
        click.echo(f"{BOLD}You're not logged in! Log in to init a repo with brwne 🫡{RESET}")
        return

    if not GitEngine.clone_repo(repo_url):
        click.echo(f"{RED}{BOLD}Error: Could not clone the repository{RESET}")
        return
    
    # getting the repo id
    repo_id = get_repo_id(repo_remote_url=repo_url.replace(".git", ""))

    # checking if the repo_id is in the database
    if curr_repo_data := RealtimeDBEngine().read_data(f"repos/{repo_id}"):
        # adding this repo to the user's list of repos
        if uid := RealtimeDBEngine().get_UID():
            RealtimeDBEngine().write_data(f"user_repos/{uid}/{repo_id}", {
                    "last_cloned": int(time.time())
                })
            
            
            # Create .brwne directory inside the cloned repository
            repo_name = curr_repo_data['repo_name']
            brwne_dir = os.path.join(repo_name, ".brwne")
            os.makedirs(brwne_dir, exist_ok=True)
            
            # Write the repo_id to a file inside the .brwne directory
            with open(os.path.join(brwne_dir, "repo_id.txt"), "w") as f:
                f.write(repo_id)
        
            click.echo(f"{GREEN}{BOLD}Successfully cloned {curr_repo_data['repo_name']}! Your all set :){RESET}")
        else:
            print(f"{RED}{BOLD}Unable to fetch your UID, we clone the repo but could not set up brwne for you{RESET}")
    else:
        repo_folder_name = get_repo_folder_name(repo_url=repo_url)

        click.echo(
        f"\n{BOLD}brwne hasn't seen this repo before, {RESET}"
        f"{BOLD}Run the following commands to set it up with brwne!{RESET}\n\n"
        f"{BLACK_BG_WHITE_TEXT}cd {repo_folder_name} && brwne init{RESET}\n"
        )

        


    

    