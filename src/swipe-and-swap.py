import os
import shutil
import sys
import requests
import argparse
from urllib.parse import urlparse

# Get Cadence from a repo
def swipe(owner, repo_name, branch, dest_dir):
    print(f'Swiping Cadence from {owner}/{repo_name}/{branch} to {dest_dir}...')
    # Define the directories to copy
    dirs_to_copy = ["contracts", "scripts", "transactions"]

    # Overwrite the existing directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Loop through each directory and copy its contents to the cadence directory
    for directory in dirs_to_copy:
        # Construct the URL for the directory's contents API
        dir_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{directory}?ref={branch}"
        print(f'Getting {directory} from {dir_url}')
        response = requests.get(dir_url)

        # If the request was unsuccessful, print an error message and exit
        if response.status_code != 200:
            print(f"Error: Could not access {dir_url}")
            sys.exit()

        # Create the directory if it doesn't exist
        dest_sub_dir = os.path.join(dest_dir, directory)
        if not os.path.exists(dest_sub_dir):
            os.makedirs(dest_sub_dir)

        # Loop through each item in the directory and copy it to the cadence directory
        for item in response.json():
            if item["type"] == "file":
                # If the item is a file, copy it to the cadence directory
                file_url = item["download_url"]
                response = requests.get(file_url)

                # If the request was unsuccessful, print an error message and continue to the next item
                if response.status_code != 200:
                    print(f"Error: Could not access {file_url}")
                    continue

                # Construct the file path for the cadence directory and copy the file
                file_path = os.path.join(dest_sub_dir, item["name"])
                with open(file_path, "wb") as f:
                    f.write(response.content)
            elif item["type"] == "dir":
                # If the item is a directory, copy all its contents to the cadence directory
                subdir_url = item["url"]
                subdir_response = requests.get(subdir_url)

                # If the request was unsuccessful, print an error message and continue to the next item
                if subdir_response.status_code != 200:
                    print(f"Error: Could not access {subdir_url}")
                    continue

                # Create the subdirectory in the cadence directory
                subdir_name = item["name"]
                subdir_dest_dir = os.path.join(dest_sub_dir, subdir_name)
                os.makedirs(subdir_dest_dir, exist_ok=True)

                # Loop through each item in the subdirectory and copy it to the cadence directory
                for subdir_item in subdir_response.json():
                    if subdir_item["type"] == "file":
                        file_url = subdir_item["download_url"]
                        response = requests.get(file_url)

                        # If the request was unsuccessful, print an error message and continue to the next item
                        if response.status_code != 200:
                            print(f"Error: Could not access {file_url}")
                            continue
                    # Construct the file path for the cadence directory and copy the file
                    file_path = os.path.join(subdir_dest_dir, subdir_item["name"])
                    with open(file_path, "wb") as f:
                        f.write(response.content)
    print(f'Swiping complete! On to Swapping...')

# Swap local Cadence to JS or TS
def swap(cadence_dir, dest_dir):
    print(f'Swapping from {cadence_dir} to {dest_dir}...')

    # Create the src/cadence directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Loop through all files and directories in the cadence directory
    for root, dirs, files in os.walk(cadence_dir):
        # Construct the corresponding subdirectory in the src/cadence directory
        # Remove the cadence/ prefix from the root path
        subdir = root[len(cadence_dir):]
        subdir_dest_dir = os.path.join(dest_dir, subdir)
        if not os.path.exists(subdir_dest_dir):
            os.makedirs(subdir_dest_dir)
        # Loop through all files in the current directory
        for file_name in files:
            if file_name.endswith(".cdc"):
                # Construct the file paths
                file_path = os.path.join(root, file_name)
                dest_file_path = os.path.join(
                    subdir_dest_dir, file_name[:-4] + ".ts")

                # Read the contents of the cadence file and save it to a typescript constant
                with open(file_path, "r") as cadence_file, open(dest_file_path, "w") as ts_file:
                    contents = cadence_file.read()
                    const_name = file_name[:-4].replace("-", "_").upper()
                    ts_file.write(f"const {const_name} = `{contents}`\n\n")
                    ts_file.write(f"export default {const_name}\n")

            else:
                # Copy non-cadence files directly to the destination directory
                file_path = os.path.join(root, file_name)
                dest_file_path = os.path.join(subdir_dest_dir, file_name)
                shutil.copy2(file_path, dest_file_path)
    print(f'Swapping complete!')


def main():
    """
    Add & assign args
    """
    # Parse the GitHub repository, target branch, and destination directory from the given arguments
    parser = argparse.ArgumentParser(description="Copy contracts, scripts, and transactions from a GitHub repository & swap to TypeScript consts")
    parser.add_argument("--action", help="Action to perform - swipe/swap/both (default is both)", default="both")
    parser.add_argument("--repo", help="owner/name of the Cadence repo")
    parser.add_argument("--branch", help="Name of the branch to clone (default is main)", default="main")
    parser.add_argument("--swipe-dest", help="Name of the directory to save to", default="cadence/")
    parser.add_argument("--swap-dest", help="Directory to save your .ts files to (default is src/cadence)", default="src/cadence/")
    args = parser.parse_args()
    # Assign args
    action = args.action
    parsed_url = urlparse(args.repo)
    branch = args.branch
    swipe_dest = args.swipe_dest
    try:
        if action in ["swipe", "both"]:
            owner, repo_name = parsed_url.path.strip('/').split('/')
    except:
        print("[ERROR]: Must specify repo when swiping Cadence!")
        exit()
    cadence_dir = swipe_dest
    swap_dest = args.swap_dest

    """
    Swipe & Swap
    """
    if action in ["swipe", "both"]:
        # Get Cadence
        swipe(owner, repo_name, branch, swipe_dest)
    if action in ["swap", "both"]:
        # Swap local files
        swap(cadence_dir, swap_dest)

if __name__ == '__main__':
    main()
