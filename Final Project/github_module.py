import subprocess
import os

def clone_github_repo(repo_url="https://github.com/dylanbuchi/31-days-of-code.git", clone_directory="cloned_repo"):
    """
    Clones a GitHub repository to a specified directory.
    """
    if os.path.exists(clone_directory):
        print(f"Directory {clone_directory} already exists, skipping cloning.")
    else:
        subprocess.run(["git", "clone", repo_url, clone_directory], check=True)
        print(f"Cloned repository to {clone_directory}")