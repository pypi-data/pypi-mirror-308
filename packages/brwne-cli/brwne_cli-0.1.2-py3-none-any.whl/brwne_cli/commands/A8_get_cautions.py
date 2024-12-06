import re

from brwne_cli.gitEngine import GitEngine
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData
from brwne_cli.utils.ANSI_Colors import *

# TODO: were currently ignoreing the current branch the user is one, 
# do not do this as the remote version of current branch may have changes (that we dont have)

### HELPER FUNCTIONS ###

# 1. split_branch_diff_into_files
#     - you get a massive diff for another branch from the last common commit to the latest commit on that branch
#     - this function uses the file headers to split the diff into sections based on the file changes

# 2. split_file_diff_into_hunks
#     - this function uses the hunk headers to split the file diff into hunk sections
#     - a hunk is a section of a diff that shows the changes made to a specific part of a file (consecutive lines usually)

# 3. parse_git_diff_u0_header
#     - this function parses a git diff header line in the `-U0` format to determine the ranges of added and removed lines
#     - the function expects headers of the form: @@ -<old_line_start>,<old_count> +<new_line_start>,<new_count> @@


def split_branch_diff_into_files(diff_text: str):
    # Regular expression to match the start of a file change section and capture the file path
    file_change_pattern = r"diff --git a/([\w/.-]+) b/[\w/.-]+"

    # Split the diff into sections based on the file change pattern
    file_changes = re.split(file_change_pattern, diff_text)

    # Parse the sections into file paths and contents
    file_changes_with_paths = []
    for i in range(1, len(file_changes), 2):
        filepath = file_changes[i]
        file_content = f"diff --git a/{filepath} b/{filepath}\n{file_changes[i + 1].strip()}"
        file_changes_with_paths.append({"filepath": filepath, "content": file_content})

    return file_changes_with_paths

def split_file_diff_into_hunks(file_diff: str, branch_name: str):
    # Updated regex pattern to match hunk headers with optional line counts
    hunk_pattern = r"(@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@)"

    # Split the file diff into hunk sections based on the hunk header
    hunk_sections = re.split(hunk_pattern, file_diff)

    # Collect hunks with headers and content
    hunks = []
    for i in range(1, len(hunk_sections), 2):
        header = hunk_sections[i].strip()
        content_lines = hunk_sections[i + 1].strip().splitlines()
        hunks.append({"header": header, "content": content_lines, "branch": branch_name})

    return hunks

def parse_git_diff_u0_header(header: str) -> dict:
    """
    Parses a git diff header line in the `-U0` format to determine the ranges of added and removed lines.

    The function expects headers of the form:
    @@ -<old_line_start>,<old_count> +<new_line_start>,<new_count> @@
    
    - `old_line_start`: The starting line number of the original (removed) lines.
    - `old_count`: The number of lines removed (if omitted, defaults to 1).
    - `new_line_start`: The starting line number of the new (added) lines.
    - `new_count`: The number of lines added (if omitted, defaults to 1).
    
    Parameters:
    - header (str): A git diff header line in the `-U0` format.

    Returns:
    - dict: A dictionary with the following keys:
        - `added`: A list [start, end] indicating the range of added lines, or `None` if no lines were added.
        - `removed`: A list [start, end] indicating the range of removed lines, or `None` if no lines were removed.
        
    Examples:
    Given the input header "@@ -5,3 +5,3 @@":
    The function will return `{'added': [5, 7], 'removed': [5, 7]}`.

    Given the input header "@@ -8 +7,0 @@":
    The function will return `{'added': None, 'removed': [8, 8]}`.

    Given the input header "@@ -4,0 +5 @@":
    The function will return `{'added': [5, 5], 'removed': None}`.

    """
    # Regex pattern to extract line numbers and counts from the header
    pattern = r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@'
    match = re.match(pattern, header)
    
    if match:
        # Extract values from regex match groups, using default of 1 if no count is specified
        old_start = int(match.group(1))
        old_count = int(match.group(2)) if match.group(2) else 1
        new_start = int(match.group(3))
        new_count = int(match.group(4)) if match.group(4) else 1
        
        # Determine the removed range if any
        removed = [old_start, old_start + old_count - 1] if old_count > 0 else None
        
        # Determine the added range if any
        added = [new_start, new_start + new_count - 1] if new_count > 0 else None
        
        return {"added": added, "removed": removed}
    
    # Return None if the header format doesn't match
    return None

### MAIN FUNCTION ###
@pre_command()
def get_cautions(context: CommandContextData):

    # we do analysis on remote branches first (unpushed diffs are later...)
    remote_branches = GitEngine.get_remote_branches()

    name_of_remote = remote_branches[0].split("/")[0]   # get the name of the remote (usually origin)

    # get the current branch
    current_branch = GitEngine.get_current_branch()
    remote_branches.remove(f"{name_of_remote}/{current_branch}")

    print(f"current branch: {current_branch}, remote branches: {remote_branches}")

    # getting the last common commit between us and the latest version of the remote branch'
    GitEngine.fetch()

    diff_data = {}

    for branch in remote_branches:
        last_common_commit = GitEngine.get_merge_base(current_branch, branch)
        diff = GitEngine.get_diff_from_commit_to_latest(last_common_commit, branch)    

        # Split the diff into file changes
        file_diffs = split_branch_diff_into_files(diff_text=diff)

        if len(file_diffs) == 0:
            continue
        else:
            # Display each file change section
            for index, change in enumerate(file_diffs, start=1):

                # get the filename from the diff
                filename = change['filepath']
                file_diff = change['content']

                # getting the hunks from the file diff
                hunks = split_file_diff_into_hunks(file_diff, branch);

                if len(hunks) != 0:
                    if filename not in diff_data:
                        diff_data[filename] = []

                    for hunk in hunks:
                        hunk_header = hunk['header']
                        added_and_removed_ranges = parse_git_diff_u0_header(hunk_header)
                        hunk["added"] = added_and_removed_ranges["added"]
                        hunk["removed"] = added_and_removed_ranges["removed"]
                    
                    diff_data[filename].extend(hunks)
    
    print(diff_data);


