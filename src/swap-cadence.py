import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Translate contracts, scripts, and transactions from your local directory to TypeScript constants")
parser.add_argument("--source-dir", help="Directory holding your .cdc files (default is cadence/)", default="cadence/")
parser.add_argument("--dest", help="Directory to save your .ts files to (default is src/cadence)", default="src/cadence/")
args = parser.parse_args()
cadence_dir = args.source_dir
dest_dir = args.dest

# Create the src/cadence directory if it doesn't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Loop through all files and directories in the cadence directory
for root, dirs, files in os.walk(cadence_dir):
    # Construct the corresponding subdirectory in the src/cadence directory
    subdir = root[len(cadence_dir):]  # Remove the cadence/ prefix from the root path
    subdir_dest_dir = os.path.join(dest_dir, subdir)
    if not os.path.exists(subdir_dest_dir):
        os.makedirs(subdir_dest_dir)

    # Loop through all files in the current directory
    for file_name in files:
        if file_name.endswith(".cdc"):
            # Construct the file paths
            file_path = os.path.join(root, file_name)
            dest_file_path = os.path.join(subdir_dest_dir, file_name[:-4] + ".ts")

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