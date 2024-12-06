import subprocess
from typing import Optional, List, Union, Callable
import hashlib

from brwne_cli.utils.ANSI_Colors import *

# Method Index:
# - is_inside_git_repo: Check if the current directory is inside a git repository.
# - get_repo_remote_url: Get the remote URL of the repository.
# - get_repo_id: Get a unique identifier for the repository based on its remote URL.
# - get_remote_branches: Get a list of all remote branches.
# - get_latest_commit: Get the latest commit hash for a specified remote branch.
# - get_current_branch: Get the name of the current branch.
# - add_files: Add specified files to the staging area.
# - create_switch_and_push_branch: Create a new branch and push it to the remote.
# - switch_to_branch: Switch to a specified branch.
# - commit_changes: Commit changes on the current branch with a provided message.
# - get_diff_between_commits: Get the diff between two commits in patch format.
# - get_parent_commit: Get the parent commit of a specified commit.
# - get_status: Get the status of the current working directory.
# - fetch_all: Fetch all branches from the remote.
# - pull_all: Pull all branches from the remote.
# - push_commits: Push commits from the current branch to the remote.
# - get_commits_to_push: Get a list of commits that are about to be pushed.
# - fetch: Fetch the latest updates from the remote repository.
# - get_merge_base: Get the last common commit hash between two branches.
# - get_diff_from_commit_to_latest: Get the diff in patch mode from a commit to the latest commit on a branch.
# - count_unpushed_commits: Count the number of commits that have not yet been pushed to the remote repository. (returns -1 if error)
# - clone_repo: Clone a repository from a given URL. (returns True if successful, False otherwise)
# - unpulled_commits_count_from_branch: Get the number of unpulled commits for a specified branch. (returns 0 if up to date or error)
# - simulate_rebase: Simulate a rebase with the specified branch to check for conflicts. (returns True if no conflicts, False otherwise)
# - perform_rebase: Perform a rebase onto the specified branch. (returns True if successful, False if conflicts or error)
# - stash_current_working_changes: Stash current working changes and return a function to unstash them later. (returns 0 if no changes, Callable if successful, None if error)
# - rebase_down: Rebase branch_to onto branch_from and push with --force


class GitEngine:
    @staticmethod
    def is_inside_git_repo() -> bool:
        """
        Check if the current directory is inside a git repository.

        This function runs a git command to check if the current directory
        is inside a git working tree.

        Returns:
            bool: True if the current directory is inside a git repository, False otherwise.
        """
        command = ["git", "rev-parse", "--is-inside-work-tree"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    @staticmethod
    def get_repo_remote_url() -> Optional[str]:
        """
        Get the repository's remote URL.

        This function runs a git command to retrieve the URL of the remote repository
        named 'origin'.

        Returns:
            str: The remote URL of the repository, or an empty string if the URL cannot be retrieved.
        """
        command = ["git", "remote", "get-url", "origin"]
        result = subprocess.run(command, capture_output=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip().decode('utf-8').rstrip(".git")
            return remote_url
        return None
    
    @staticmethod
    def get_repo_id(repo_remote_url: Optional[str] = None) -> Optional[str]:
        """
        Get the repository's id (which is computed by taking the remote url then hashing it).
        if the remote url is not given, it will use git commands to find it
        expects repo url to be without the '.git' extension at the end

        runs the get_repo_remote_url function to get the remote url of the repository, then uses hashlib to hash it

        Returns:
            str: The remote URL of the repository, or None if the URL cannot be retrieved.
        """
        if repo_remote_url is None or repo_remote_url == "":
            repo_remote_url = GitEngine.get_repo_remote_url()

        if repo_remote_url:
            secret = "brownies4life"    # this is not really a secret, just a random string to make the hash unique (ish)
            repo_remote_url += secret   # its a gimmick, for the lols
            repo_id = hashlib.sha256(repo_remote_url.encode()).hexdigest()
            return repo_id

        return None

    @staticmethod
    def get_remote_branches() -> Optional[List[str]]:
        # Step 1: Detect the default remote name
        remote_name_cmd = ["git", "remote"]
        remote_result = subprocess.run(remote_name_cmd, capture_output=True, text=True)
        
        if remote_result.returncode != 0:
            # Return None if we couldn't determine the remote name
            return None
        
        # Assume the first remote listed is the default (usually 'origin')
        remote_name = remote_result.stdout.strip().split("\n")[0]
        
        # Step 2: List remote branches
        branch_command = ["git", "branch", "-r"]
        branch_result = subprocess.run(branch_command, capture_output=True, text=True)
        
        if branch_result.returncode == 0:
            # Split output into lines and filter out the HEAD reference
            branches = branch_result.stdout.strip().split("\n")
            branches = [
                branch.strip() for branch in branches 
                if f"{remote_name}/HEAD ->" not in branch
            ]
            return branches
        
        # Return None if branch command failed
        return None
    
    @staticmethod
    def get_latest_commit(branch: str) -> Optional[str]:
        """
        Get the latest commit hash for a specific remote branch.

        Args:
            branch (str): The remote branch name (e.g., 'origin/main').

        Returns:
            str: The latest commit hash of the branch, or None if there is an error.
        """
        command = ["git", "rev-parse", branch]
        result = subprocess.run(command, capture_output=True)

        if result.returncode == 0:
            latest_commit = result.stdout.strip().decode('utf-8')
            return latest_commit

        return None

    @staticmethod
    def get_current_branch() -> Optional[str]:
        """
        Get the name of the current branch.

        This function runs a git command to get the name of the current branch.

        Returns:
            str: The name of the current branch, or None if it cannot be determined.
        """
        command = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        result = subprocess.run(command, capture_output=True)
        if result.returncode == 0:
            branch_name = result.stdout.strip().decode('utf-8')
            return branch_name
        return None
    
    @staticmethod
    def add_files(files: list) -> int:
        """
        Add the specified files to the staging area.

        This function runs a git command to add the specified files to the staging area.

        Args:
            files (List[str]): A list of files or directories to add.

        Returns:
            int: The number of files successfully added.
        """
        if not files:
            return 0
        command = ["git", "add"] + list(files)
        result = subprocess.run(command, capture_output=True)
        if result.returncode == 0:
            # Count the number of files staged
            status_command = ["git", "diff", "--cached", "--name-only"]
            status_result = subprocess.run(status_command, capture_output=True, text=True)
            if status_result.returncode == 0:
                added_files = status_result.stdout.splitlines()
                return len(added_files)
        return 0


    @staticmethod
    def create_switch_and_push_branch(new_branch_name: str) -> bool:
        """
        Create a new branch from the current branch and push it to the remote.

        This function runs git commands to create a new branch from the current branch
        and then push the new branch to the remote repository.

        Args:
            new_branch_name (str): The name of the new branch to create.

        Returns:
            bool: True if the branch was successfully created and pushed, False otherwise.
        """
        # Create the new branch
        command_create_branch = ["git", "checkout", "-b", new_branch_name]
        result_create_branch = subprocess.run(command_create_branch, capture_output=True)
        if result_create_branch.returncode != 0:
            return False

        # Push the new branch to remote
        command_push_branch = ["git", "push", "-u", "origin", new_branch_name]
        result_push_branch = subprocess.run(command_push_branch, capture_output=True)
        return result_push_branch.returncode == 0

    @staticmethod
    def switch_to_branch(branch_name: str) -> bool:
        """
        Switch to the specified branch.

        This function runs a git command to switch to the specified branch.

        Args:
            branch_name (str): The name of the branch to switch to.

        Returns:
            bool: True if the branch was successfully switched, False otherwise.
        """
        command = ["git", "checkout", branch_name]
        result = subprocess.run(command, capture_output=True)
        return result.returncode == 0

    @staticmethod
    def commit_changes(commit_message: str) -> Optional[str]:
        """
        Commit the changes on the current branch with the provided commit message.

        This function runs a git command to commit the staged changes and returns the commit hash.

        Args:
            commit_message (str): The commit message to use for the commit.

        Returns:
            str: The commit hash of the new commit, -1 if no files are being tracked, or None if there was an error.
        """
        # Check if there are changes to commit
        command_status = ["git", "status", "--porcelain"]   # porcelain format for easy parsing (no color, machine-readable)
        result_status = subprocess.run(command_status, capture_output=True)
        if result_status.returncode != 0 or not result_status.stdout.strip():
            return -1

        # Commit the changes
        command_commit = ["git", "commit", "-m", commit_message]
        result_commit = subprocess.run(command_commit, capture_output=True)
        if result_commit.returncode != 0:
            return None

        # Get the commit hash of the latest commit
        command_get_commit_hash = ["git", "rev-parse", "HEAD"]
        result_hash = subprocess.run(command_get_commit_hash, capture_output=True)
        if result_hash.returncode == 0:
            commit_hash = result_hash.stdout.strip().decode('utf-8')
            return commit_hash

        return None
    
    @staticmethod
    def get_diff_between_commits(commit1: str, commit2: str) -> Optional[str]:
        """
        Get the diff between two commits in patch format.

        This function runs a git command to get the diff between two specified commits and returns it in patch format.

        Args:
            commit1 (str): The hash of the first commit.
            commit2 (str): The hash of the second commit.

        Returns:
            str: The diff between the two commits in patch format, or None if there was an error.
        """
        command_diff = ["git", "diff", commit1, commit2, "--patch"]
        result_diff = subprocess.run(command_diff, capture_output=True)
        if result_diff.returncode == 0:
            diff_output = result_diff.stdout.strip().decode('utf-8')
            return diff_output
        return None

    @staticmethod
    def get_parent_commit(commit: str) -> Optional[str]:
        """
        Get the parent commit of a specified commit.

        This function runs a git command to get the hash of the parent commit of the specified commit.

        Args:
            commit (str): The hash of the commit whose parent is to be retrieved.

        Returns:
            str: The hash of the parent commit, or None if there was an error.
        """
        command_parent = ["git", "rev-parse", f"{commit}^"]
        result_parent = subprocess.run(command_parent, capture_output=True)
        if result_parent.returncode == 0:
            parent_commit = result_parent.stdout.strip().decode('utf-8')
            return parent_commit
        return None
    
    @staticmethod
    def get_status() -> Optional[str]:
        """
        Get a comprehensive and formatted status of the current working directory.

        Returns:
            str: The formatted status of the working directory, or None if there was an error.
        """
        command_status = ["git", "status", "--porcelain"]
        result_status = subprocess.run(command_status, capture_output=True, text=True)

        if result_status.returncode == 0:
            status_output = result_status.stdout.strip()
            if not status_output:
                return "No changes in working directory to track! 😃"
            
            # Lists to hold different categories of changes
            staged = []
            unstaged = []
            untracked = []
            conflicted = []

            for line in status_output.split('\n'):
                # Check for untracked files (indicated by ??)
                if line.startswith("??"):
                    untracked.append(f"untracked:  {(line.rstrip()).split(' ')[-1]}")
                    continue

                # Parse index and worktree statuses
                index_status = line[0]
                worktree_status = line[1]
                print(index_status, worktree_status)
                file_path = (line.rstrip()).split(" ")[-1]

                # Handle staged changes
                if index_status == 'M':
                    staged.append(f"modified:   {file_path}")
                elif index_status == 'A':
                    staged.append(f"added:      {file_path}")
                elif index_status == 'D':
                    staged.append(f"deleted:    {file_path}")
                elif index_status == 'R':
                    old, new = file_path.split(" -> ")
                    staged.append(f"renamed:    {old} -> {new}")
                elif index_status == 'C':
                    staged.append(f"copied:     {file_path}")
                
                # Handle unstaged changes
                if worktree_status == 'M':
                    unstaged.append(f"modified:   {file_path}")
                elif worktree_status == 'D':
                    unstaged.append(f"deleted:    {file_path}")
                
                # Handle conflicted files
                if index_status == 'U' or worktree_status == 'U':
                    conflicted.append(f"conflicted: {file_path}")

            # Format output based on categories
            output_lines = []
            
            if staged:
                output_lines.append(f"Changes to be committed: (`br commit [message]` to commit)")
                for line in staged:
                    output_lines.append(f"  {GREEN}{line}{RESET}")
                output_lines.append("")  # Blank line for readability
            
            if unstaged or untracked:
                output_lines.append("Changes not staged for commit: (br add [filename]` to stage)")
                for line in unstaged:
                    output_lines.append(f"  {RED}{line}{RESET}")
                for line in untracked:
                    output_lines.append(f"  {RED}{line}{RESET}")
                output_lines.append("")
            
            if conflicted:
                output_lines.append("Conflicted paths:")
                for line in conflicted:
                    output_lines.append(f"  {BOLD}{RED}{line}{RESET}")
                output_lines.append("")

            return "\n".join(output_lines)
        
        else:
            return None
        
    @staticmethod
    def fetch_all():
        import subprocess
        try:
            subprocess.run(["git", "fetch", "--all", "--prune"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during fetching branches: {e}")

    @staticmethod
    def pull_all():
        import subprocess
        try:
            subprocess.run(["git", "pull", "--all"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during pulling branches: {e}")
    
    @staticmethod
    def push_commits() -> bool:
        """
        Push the commits of the current branch to the remote.

        This function runs a git command to push the commits from the current branch to the remote repository.

        Returns:
            bool: True if the push was successful, False otherwise.
        """
        command_push = ["git", "push"]
        result_push = subprocess.run(command_push, capture_output=True)
        return result_push.returncode == 0

    @staticmethod
    def get_commits_to_push() -> Optional[List[str]]:
        """
        Get a list of commits that are about to be pushed to the remote repository.

        This function runs a git command to get the list of commits that are on the current branch but not yet pushed to the remote.

        Returns:
            List[str]: A list of full commit hashes that are about to be pushed, or None if there was an error.
        """
        command_log = ["git", "log", "@{u}..", "--pretty=format:%H"]
        result_log = subprocess.run(command_log, capture_output=True)
        if result_log.returncode == 0:
            commits = result_log.stdout.strip().decode('utf-8').splitlines()
            return reversed(commits)    # latest commit is last after reversing
        return None
    
    @staticmethod
    def fetch_branch(branch_to_fetch):
        """
        Fetches the specified branch from the remote repository.
        """
        try:
            subprocess.run(
                ['git', 'fetch', 'origin', f"{branch_to_fetch}:{branch_to_fetch}"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error while fetching branch {branch_to_fetch}: {e}")

    @staticmethod
    def fetch():
        """
        Fetches the latest updates from the remote repository.
        No printing because its used in cautions
        """
        try:
            subprocess.run(
                ['git', 'fetch', 'origin'],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            pass

    @staticmethod
    def get_merge_base(branch1, branch2):
        """
        Returns the last common commit hash between two branches.
        """
        try:
            result = subprocess.run(
                ['git', 'merge-base', branch1, branch2],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error while getting merge base between {branch1} and {branch2}: {e}")
            return None
    
    @staticmethod
    def get_diff_from_commit_to_latest(commit, branch):
        """
        Returns the diff in patch mode from the specified commit to the latest commit on the given branch.
        """
        try:
            # Use git diff command with --patch option to get the diff in patch mode
            result = subprocess.run(
                ['git', '--no-pager', 'diff', '-U0', f'{commit}..{branch}', '--patch'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error while getting diff from commit {commit} to branch {branch} in patch mode: {e}")
            return None
    
    @staticmethod
    def count_unpushed_commits() -> int:
        """
        Count the number of commits that have not yet been pushed to the remote repository.

        This function runs a git command to get the list of commits that are on the current branch
        but not yet pushed to the remote.

        Returns:
            int: The number of unpushed commits, or -1 if there was an error.
        """
        command = ["git", "log", "@{u}..", "--pretty=oneline"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            unpushed_commits = result.stdout.strip().splitlines()
            return len(unpushed_commits)
        return -1

    @staticmethod
    def clone_repo(repo_url: str) -> bool:
        """
        Clone a repository from a given URL.

        Args:
            repo_url (str): The URL of the repository to clone.

        Returns:
            bool: True if cloning was successful, False otherwise.
        """
        command = ["git", "clone", repo_url]
        result = subprocess.run(command, capture_output=True)

        if result.returncode == 0:
            return True  # Cloning was successful
        else:
            # Print error details for debugging purposes
            print(f"Failed to clone the repository. Error: {result.stderr.decode('utf-8')}")
            return False
        
    @staticmethod
    def unpulled_commits_count_from_branch(branch_name: str = 'main') -> int:
        """
        Get the number of unpulled commits for the specified branch.
        NOTE: Make sure you run git fetch before running this function.

        Args:
            branch_name (str): The name of the branch to check. Defaults to 'main'.

        Returns:
            int: The number of unpulled commits. Returns 0 if up to date or if an error occurs.
        """

        # Count the number of unpulled commits
        count_command = ["git", "rev-list", "--count", f"HEAD..origin/{branch_name}"]
        try:
            count_result = subprocess.run(count_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            unpulled_count = int(count_result.stdout.strip())
            return unpulled_count
        except (subprocess.CalledProcessError, ValueError):
            return 0
    
    @staticmethod
    def attempt_rebase(branch_name: str) -> bool:
        """
        Simulate a rebase with the specified branch to check for conflicts.
        NOTE: Make sure you run git fetch before running this function.

        Args:
            branch_name (str): The name of the branch to rebase onto. Defaults to 'main'.

        Returns:
            bool: True if no conflicts, False if conflicts are detected or an error occurs.
        """
        rebase_command = ["git", "rebase", f"origin/{branch_name}"]
        try:
            # Simulate the rebase
            subprocess.run(rebase_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True  # No conflicts detected
        except subprocess.CalledProcessError:
            # Abort the rebase in case of conflicts
            subprocess.run(["git", "rebase", "--abort"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            return False  # Conflicts detected
    
    @staticmethod
    def perform_rebase_from_origin(branch_name: str = 'main') -> bool:
        """
        Perform a rebase onto the specified branch.
        NOTE: Make sure you run git fetch before running this function.

        Args:
            branch_name (str): The name of the branch to rebase onto. Defaults to 'main'.

        Returns:
            bool: True if the rebase completes successfully, False if conflicts are detected or an error occurs.
        """
        rebase_command = ["git", "rebase", f"origin/{branch_name}"]
        try:
            # Perform the rebase
            subprocess.run(rebase_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True  # Rebase completed successfully without conflicts
        except subprocess.CalledProcessError:
            # Handle conflicts or rebase failure
            print("Rebase encountered conflicts. Please resolve them manually.")
            return False  # Conflicts detected or rebase failed
    
    @staticmethod
    def stash_current_working_changes() -> Union[int, Callable[[], bool], None]:
        """
        Stash current working changes and return a function to unstash them at a later time.

        Returns:
            Union[int, Callable[[], bool], None]:
                - 0 if there are no changes to stash.
                - Callable[[], bool] if stashing was successful, which can be called to unstash the changes.
                - None if an error occurs during stashing.
        """
        # Step 1: Check if there are changes to stash
        status_command = ["git", "status", "--porcelain"]
        try:
            result = subprocess.run(status_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            if not result.stdout.strip():
                # No changes to stash
                print("No changes to stash.")
                return 0
        except subprocess.CalledProcessError:
            print("Failed to check the status of the repository.")
            return None

        # Step 2: Stash the current changes and get the stash ID
        stash_command = ["git", "stash", "push", "-u"]  # -u includes untracked files
        try:
            result = subprocess.run(stash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            stash_output = result.stdout.decode().strip()

            # Extract stash ID from the output (usually in the format "Saved working directory and index state WIP on branch-name: <commit-hash> <message>")
            if "WIP on" in stash_output:
                stash_id = "stash@{0}"
                print(f"Changes stashed successfully with ID: {stash_id}")
            else:
                print("Failed to parse stash output.")
                return None

            # Return an unstash function that uses the specific stash ID
            def unstash_changes() -> bool:
                """
                Unstash the previously stashed changes using the specific stash ID.

                Returns:
                    bool: True if unstashing is successful, False otherwise.
                """
                unstash_command = ["git", "stash", "pop", stash_id]
                try:
                    subprocess.run(unstash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    return True  # Unstashing successful
                except subprocess.CalledProcessError:
                    print("Failed to unstash changes.")
                    return False  # Unstashing failed

            return unstash_changes

        except subprocess.CalledProcessError:
            print("Failed to stash changes.")
            return None
    
    @staticmethod
    def rebase_down(branch_from, branch_to, push_lower_branch_after_rebase=True) -> bool:
        """Attempts to rebase branch_to onto branch_from and pushes with --force-with-lease if successful.

        Args:
            branch_from (str): The branch to rebase onto (e.g., 'main').
            branch_to (str): The branch to be rebased (e.g., 'dev').
            push_lower_branch_after_rebase (bool): Whether to push the lower branch after a successful rebase. Defaults to True.

        Returns:
            bool: True if the rebase and push were successful, False if conflicts or errors occurred.
        """
        try:
            # 1. Fetch the latest changes from remote
            print("Fetching latests changes from remote...")
            fetch_command = ["git", "fetch", "origin"]
            subprocess.run(fetch_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 2. Checkout the 'to' branch
            print(f"Checking out {branch_to} branch...")
            checkout_command = ["git", "checkout", branch_to]
            subprocess.run(checkout_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 3. Attempt to rebase 'to' branch onto 'from' branch
            print(f"Attempting to rebase {branch_to} onto {branch_from}...")
            rebase_command = ["git", "rebase", f"origin/{branch_from}"]
            try:
                subprocess.run(rebase_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Rebase of {branch_to} onto {branch_from} successful!")
            except subprocess.CalledProcessError:
                # If rebase fails, abort the rebase and notify the user
                abort_command = ["git", "rebase", "--abort"]
                subprocess.run(abort_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return False

            # 4. Push the rebased 'to' branch with --force-with-lease
            if push_lower_branch_after_rebase:
                print(f"Pushing {branch_to} with --force-with-lease...")
                push_command = ["git", "push", "--force-with-lease", "origin", branch_to]
                subprocess.run(push_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print(f"Rebase of {branch_to} onto {branch_from} completed and pushed successfully!")
            return True

        except subprocess.CalledProcessError as e:
            # General error handling if any command fails outside of rebase conflicts
            print(f"An error occurred: {e.stderr.decode()}")
            return False