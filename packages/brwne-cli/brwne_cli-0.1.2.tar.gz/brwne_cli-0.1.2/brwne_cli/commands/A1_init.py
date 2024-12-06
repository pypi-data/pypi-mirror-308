"""
Command for Initializing Brownie with Git.

Gives you two options, either to create a new repo with brwne or initialise from a current git repo 🚫(not allowed yet...). 
Usage:
    Run the `brwne init` command within a Git repository to initialize it with Brownie.

Functions:
    init_command(args): Main function to initialize the repository with Brownie.
"""

import click
import re
import time
import os
import subprocess

from brwne_cli.commands.auth import user_is_logged_in
from brwne_cli.gitEngine import GitEngine
from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.ANSI_Colors import *

# cannot have a pre_command decorator here as brwne isnt set up yet
def init_command():
    # Step 1: Check if user is logged in
    if not user_is_logged_in():
        click.echo(f"{BOLD}You're not logged in mate! Log in to init a repo with brwne 🫡{RESET}")
        return
    
    # Step 2: Check if user is already inside a brwne repo
    if ".brwne" in os.listdir():
        click.echo(f"{BOLD}You're already inside a brwne repo 🎉{RESET}")
        return
    
    # Step 3: Check if user is inside a git repo
    if GitEngine.is_inside_git_repo():
        
        # Sync local branches with remote
        click.echo(f"{BOLD}Syncing local branches with remote...{RESET}")
        GitEngine.fetch_all()
        GitEngine.pull_all()
        
        # Step 4: Check that the user has configured a remote repo
        if remote_url := GitEngine.get_repo_remote_url():

            repo_id = GitEngine.get_repo_id(repo_remote_url=remote_url.replace(".git", ""))

            # check if this repo is already set up with brwne on our server
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
                
                    click.echo(f"{GREEN}{BOLD}Found this repo - {curr_repo_data['repo_name']} on our server, we cleaned it up and connected it to brwne! Your all set :){RESET}")
                    return
                else:
                    print(f"{RED}{BOLD}Unable to fetch your UID, found this repo on our system but we couldnt it up for you.{RESET}")
                    return
                    
            else:
                # Step 5: check that theres only one branch on the remote repo.
                remote_branches = GitEngine.get_remote_branches()
                if len(remote_branches) > 1:
                    click.echo(f"{RED}{BOLD}You have more than one branch on your remote repo! Please make sure you have only one main branch on your remote repo before initialising brwne{RESET}")
                    return
                
                else:
                    # Step 6: Create a new ID for this repo and initialise it with Brwne
                    repo_id = GitEngine.get_repo_id()

                    match = re.search(r'/([^/]+?)(?:\.git)?$', remote_url)  # Extract the repo name from the remote URL
                    repo_name = match.group(1)
                    
                    os.mkdir(".brwne")
                    with open(".brwne/repo_id.txt", "w") as f:
                        f.write(repo_id)
                    
                    # Add .brwne to .gitignore if not already present
                    if not os.path.exists(".gitignore"):
                        with open(".gitignore", "w") as gitignore_file:
                            gitignore_file.write(".brwne\n")
                    else:
                        with open(".gitignore", "r") as gitignore_file:
                            lines = gitignore_file.readlines()
                        if ".brwne\n" not in lines:
                            with open(".gitignore", "a") as gitignore_file:
                                gitignore_file.write(".brwne\n")

                    GitEngine.add_files([".gitignore"])
                    GitEngine.commit_changes("Add .brwne file to .gitignore")
                    GitEngine.push_commits()

                    # Step 7: write the repo to our database
                    RealtimeDBEngine().write_data(f"repos/{repo_id}", {
                        "repo_id": repo_id,
                        "repo_name": repo_name,
                        "remote_url": remote_url,
                        "created_at": int(time.time())
                    })

                    # Step 8: set this repo as a repo under the user
                    uid = RealtimeDBEngine().get_UID()
                    RealtimeDBEngine().write_data(f"user_repos/{uid}/{repo_id}", {
                        "created_at": int(time.time())
                    })
                    
                    # Get the latest pushed commit on a branch
                    latest_commit_on_main_branch = GitEngine.get_latest_commit(remote_branches[0])

                    # Step 9: Set up branch structure on the database
                    for branch in remote_branches:
                        branch_name = branch.split("/")[1]
                        RealtimeDBEngine().write_data(f"repo_branches/{repo_id}", {
                            branch_name: {
                                "parent": "",
                                "type": "permanent",
                                "latest_pushed_commit": latest_commit_on_main_branch,
                                "created_at": int(time.time()),
                                "last_common_commit_to_parent": ""
                            }
                        })
                    
                    click.echo(f"{BOLD}🎉🎉🎉 Successfully initialised the repo with Brownie! 🎉🎉🎉{RESET}")

        else:
            click.echo(f"{RED}{BOLD}You haven't configured a remote repo yet! Please configure a remote repo first to init brwne{RESET}")
            return

    else:
        click.echo(f"{RED}{BOLD}You're not inside a git repo 🚫, please initiaise a git repo and connect to a remote repo service like github first!{RESET}")
        return
