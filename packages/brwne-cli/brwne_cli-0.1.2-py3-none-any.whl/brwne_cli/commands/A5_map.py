import click
from enum import Enum

from brwne_cli.fireEngine import RealtimeDBEngine
from brwne_cli.utils.ANSI_Colors import *
from brwne_cli.utils.pre_command_decorator import pre_command, CommandContextData


TOTAL_WIDTH = 45
WIDTH_REDUCTION_PER_DEPTH = 4
WIDTH_INCREASE_FOR_permanent_BRANCHES = 6


# Main function to map branches
@pre_command()
def map_command(context: CommandContextData):

    # Step 4: Read the branch structure from the database
    branch_structure = RealtimeDBEngine().read_data(f"repo_branches/{context.repo_id}")

    # Find the name of the root branch
    for branch in branch_structure.keys():
        if branch_structure[branch]["parent"] == "":
            root_branch = branch
            break
    
    def add_descendants(branch, depth=0):
        children = []
        for b in branch_structure.keys():
            if branch_structure[b]["parent"] == branch:
                children.append(b)
        
        branch_structure[branch]["depth"] = depth      

        if len(children) == 0:
            return [branch]
        
        all_descendants = []
        for child in children:
            new_decendants = add_descendants(child, depth=depth+1)
            all_descendants.append(new_decendants)
        
        # sorting the descendants (temp then perm branches), secondary sort by creation time, newest first
        permanant_decendants = [d for d in all_descendants if branch_structure[d[0]]["type"] == "permanent"]
        temp_decendants = [d for d in all_descendants if branch_structure[d[0]]["type"] == "temporary"]

        permanant_decendants.sort(key=lambda x: branch_structure[x[0]]["created_at"], reverse=True)
        temp_decendants.sort(key=lambda x: branch_structure[x[0]]["created_at"], reverse=True)

        return [branch] + temp_decendants + permanant_decendants

    # Get sorted branches
    sorted_branches = add_descendants(root_branch)

    # Recursive function to print branches
    def print_branch(data, prefix="", first=False):
        curr = data[0]
        children = data[1:]

        # Determine if current branch is permanent or temporary
        is_permanent = branch_structure[curr]["type"] == "permanent"
        is_current = curr == context.current_branch

        # Check if the branch has permanent children
        has_permanent_children = False
        for child in children:
            if branch_structure[child[0]]["type"] == "permanent":
                has_permanent_children = True
                break
        
        has_children = len(children) > 0

        # Format and print the current branch label
        title = "━" if first else ""
        if has_children:
            if is_permanent and has_permanent_children:
                title += "┳"
            elif is_permanent and not has_permanent_children:
                title += "┯"
            elif not is_permanent:
                title += "┬"
        
        if(branch_structure[curr]["type"] == "permanent"):
            length_deficit = TOTAL_WIDTH - len(curr) - len(prefix) - branch_structure[curr]["depth"] * WIDTH_REDUCTION_PER_DEPTH + WIDTH_INCREASE_FOR_permanent_BRANCHES
            title += "━" * length_deficit
        else:
            length_deficit = TOTAL_WIDTH - len(curr) - len(prefix) - branch_structure[curr]["depth"] * WIDTH_REDUCTION_PER_DEPTH
            title += "─" * length_deficit

        branch_name = curr if not is_current else f"{GREEN}{BOLD}{curr} *{RESET}"
        title = prefix + title + branch_name + (f"{PURPLE}(permanent){RESET}" if is_permanent else "")

        click.echo(title)

        # Recursively print children branches
        for i, child in enumerate(children):
            child_is_permanent = (branch_structure[child[0]]["type"] == "permanent")
            if child_is_permanent:
                new_prefix = " " * branch_structure[child[0]]["depth"] + ("┣" if i < len(children) - 1 else "┗")
            else:
                if has_permanent_children:
                    new_prefix = " " * branch_structure[child[0]]["depth"] + ("┠")
                else:
                    new_prefix = " " * branch_structure[child[0]]["depth"] + ("├" if i < len(children) - 1 else "└")

            print_branch(child, new_prefix)

    # Print all branches starting from the root
    print_branch(sorted_branches, first=True)
    click.echo()
