import os
import shutil
import sys
import requests
import argparse
from urllib.parse import urlparse

# Parse the GitHub repository URL to extract the owner and repository name
parser = argparse.ArgumentParser(description="Copy contracts, scripts, and transactions from a GitHub repository")
parser.add_argument("--repo", help="owner/name of the Cadence repo")
parser.add_argument("--branch", help="Name of the branch to clone (default is main)", default="main")
args = parser.parse_args()
parsed_url = urlparse(args.repo)
branch = args.branch
owner, repo_name = parsed_url.path.strip('/').split('/')

# Construct the URL for the repository's contents API
api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents?ref={branch}"

# Define the directories to copy
dirs_to_copy = ["contracts", "scripts", "transactions"]

# Create the cadence directory if it does not already exist
cadence_dir = os.path.join(os.getcwd(), "cadence")
os.makedirs(cadence_dir, exist_ok=True)

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

    # Create the directory in the cadence directory
    dest_dir = os.path.join(cadence_dir, directory)
    print(f'Copying {directory} to {dest_dir}')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

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
            file_path = os.path.join(dest_dir, item["name"])
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
            subdir_dest_dir = os.path.join(dest_dir, subdir_name)
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