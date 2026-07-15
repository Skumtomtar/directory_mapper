import sys
from pathlib import Path

from directory import Directory


def main():
    if not len(sys.argv) == 2:
        print('Usage: python main.py "directory path"')
        sys.exit(1)

    exclusion_list = ["$RECYCLE.BIN","Derrick_project_git"]
    
    # Initialise base directory
    base_directory = Directory(Path(sys.argv[1]), exclusion_list)

    # Display exceptions
    print(f"Number of exceptions while mapping directory {base_directory.path}:\
            {len(Directory.initialisation_exceptions)}")
    for e in base_directory.initialisation_exceptions: 
        print(e)

    # Implement basic CLI to walk through the directory

if __name__ == "__main__":
    main()