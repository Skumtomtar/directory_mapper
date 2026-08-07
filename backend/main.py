import sys
import time
from pathlib import Path

from directory import Directory

"""
TODO:
    - Review behaviour of find_duplicates
        - Return second list of all duplicate files
    - Review static? for get_files_recursive
"""


FOLDER_EXCLUSION_LIST = ["$RECYCLE.BIN","Derrick_project_git"]

def display_init_exceptions(dir: Directory):
    # Displays exceptions raised during initialisation
    print(f"Number of exceptions while mapping directory {dir.path}: "
          f"{len(Directory.initialisation_exceptions)}")
    if dir.initialisation_exceptions:
        for e in dir.initialisation_exceptions: 
            print(e)


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "directory path"')
        sys.exit(1)

    
    start_time = time.perf_counter()

    # Initialise base directory
    base_directory = Directory(Path(sys.argv[1]), FOLDER_EXCLUSION_LIST)
    display_init_exceptions(base_directory)
    
    second_directory = Directory(Path(sys.argv[2]), FOLDER_EXCLUSION_LIST)
    display_init_exceptions(second_directory)

    base_dir_files = Directory.get_files_recursive(base_directory)
    second_dir_files = Directory.get_files_recursive(second_directory)
    file_list = base_dir_files + second_dir_files

    dupes = Directory.find_duplicates(file_list)

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")
    print(f"Number of duplicates found: {len(dupes)}")
    
    print("Duplicates:")
    for d in dupes:
        print(f"Path: {d.path}")
        print(f"Name: {d.name}")
        print(f"Hash: {d.hash}")
        print(f"Size: {d.size}")


if __name__ == "__main__":
    main()