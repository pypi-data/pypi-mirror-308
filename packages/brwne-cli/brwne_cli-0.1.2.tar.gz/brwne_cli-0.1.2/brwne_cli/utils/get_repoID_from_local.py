import os
def get_repo_id() -> str | None:
        """
        Get the repository's ID from the local .brwne directory.
        
        Returns:
            str: The repo ID of the repository, or None if the repo ID cannot be retrieved.
        """
        current_dir = os.getcwd()

        while current_dir != os.path.dirname(current_dir):  # Stop at the root directory
            brwne_path = os.path.join(current_dir, ".brwne", "repo_id.txt")
            if os.path.isfile(brwne_path):
                try:
                    with open(brwne_path, "r") as f:
                        repo_id = f.read().strip()
                        return repo_id
                except FileNotFoundError:
                    return None
            current_dir = os.path.dirname(current_dir)  # Move up one level

        return None

