from pathlib import Path
from file import File

class Directory:
    def __init__(self, directory_path: Path, exclusion_list: list[str] = None):
        self.path = directory_path
        self.files: dict[str, File] = {}
        self.directories: dict[str, Directory] = {}
        self.map_directory(directory_path)
    
    def map_directory(self, root_directory: Path, exclusion_list: list[str] = None):
        for item in root_directory.iterdir():
            # Skip over exclusion list
            if exclusion_list and item.name in exclusion_list:
                continue
            try:
                # If item is a file, create new File object and add this Directories file dictionary
                if item.is_file():
                    #print(item)
                    self.files[str(item)] = File(item)
                # If item is a directory, create new Directory object and add this Directories child directory dictionary
                elif item.is_dir():
                    print(item)
                    self.directories[str(item)] = Directory(item)
                    
            # Could make directory initialisation a class method, and exceptions a class attribute.
            except (FileNotFoundError,PermissionError) as e:
                print(e)


    def __str__(self):
        return "\n".join(str(item) for item in self.directories)

    def get_files(self):
        return(self.files)
    
    def get_directories(self):
        return(self.directories)
    
    def get_directories_recursive(self):
        pass