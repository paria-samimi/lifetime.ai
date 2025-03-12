import os
from glob import glob

# Get all files in a directory and subdirectories
def get_all_files(directory, extensions=("*.csv", "*.xlsx", "*.txt")):
    files = []
    for ext in extensions:
        files.extend(glob(os.path.join(directory, "**", ext), recursive=True))
    return files
