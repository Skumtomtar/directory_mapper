import sys
import time
from pathlib import Path

from directory import Directory


FOLDER_EXCLUSION_LIST = ["$RECYCLE.BIN","Derrick_project_git"]

def main():
    if not len(sys.argv) == 2:
        print('Usage: python main.py "directory path"')
        sys.exit(1)

    
    start_time = time.perf_counter()

    # Initialise base directory
    base_directory = Directory(Path(sys.argv[1]), FOLDER_EXCLUSION_LIST)

    # Display exceptions
    print(f"Number of exceptions while mapping directory {base_directory.path}: "
          f"{len(Directory.initialisation_exceptions)}")
    if base_directory.initialisation_exceptions:
        for e in base_directory.initialisation_exceptions: 
            print(e)

    dupes = base_directory.find_duplicates(Directory.get_files_recursive(base_directory))
    print("Duplicates:")
    for d in dupes:
        print(f"Name: {d.name}")
        print(f"Hash: {d.hash}")
        print(f"Size: {d.size}")

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")

    # Implement basic CLI to walk through the directory

if __name__ == "__main__":
    main()