import sys

from pathlib import Path

from file import File
from directory import Directory


def map_directory(directory: Path):
    print(f"Mapping: {directory}")
    paths = list(directory.rglob("*"))
    for path in paths:
        print(path)

        
def main():
    if not len(sys.argv) == 2:
        print("Usage: python3 main.py <directory path>")
        sys.exit(1)
    base_directory = Path(sys.argv[1])
    
    map_directory(base_directory)
    

if __name__ == "__main__":
    main()
