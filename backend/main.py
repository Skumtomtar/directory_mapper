import sys
from pathlib import Path

from directory import Directory



        
def main():
    if not len(sys.argv) == 2:
        print("Usage: python3 main.py <directory path>")
        sys.exit(1)
    base_directory = Path(sys.argv[1])
    
    
    
    exclusion_list = ["$RECYCLE.BIN"]
    
    base_directory = Directory(Path(sys.argv[1]), exclusion_list)
    

if __name__ == "__main__":
    main()
