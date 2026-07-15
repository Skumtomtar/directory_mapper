from pathlib import Path
from file import File


"""
Approach for comparing files:
Construct dictionary of files (see Generators)
Use file size as key, list of file of the same size.
    Keys with only one file in the list are unique files.
    Keys with multiple files may have duplicates and require testing
        These files should then (and only then) be hashed for comparisson
        In a loop, add files to a Set:
            if file in Set:
                append to duplicates list
            else:
                add to set
            return duplicates list
        
        Problem:
            I wish to identify the duplicate file that's already in the set
                I want to get the full path later.

"""


class Directory:
    initialisation_exceptions = []
    total_directories = 0
    total_files = 0

    def __init__(self, directory_path: Path, exclusion_list: list[str] = None):
        self.path: Path = directory_path
        self.files: dict[str, File] = {}
        self.directories: dict[str, Directory] = {}
        self.map_directory(directory_path, exclusion_list)

    # Identify Files in this directory and recursively traverse contained sub-directories
    # Append Files to list, Directories to dictionary of Directories
    def map_directory(self, root_directory: Path, exclusion_list: list[str] = None):
        for item in root_directory.iterdir():
            # Skip over exclusion list
            if exclusion_list and item.name in exclusion_list:
                continue
            try:
                # If item is a file, create new File object and add this Directories file dictionary
                if item.is_file():
                    self.files[str(item)] = File(item)
                    Directory.total_files += 1

                # If item is a directory, create new Directory object and add this Directories child directory dictionary
                elif item.is_dir():
                    self.directories[str(item)] = Directory(item)
                    Directory.total_directories += 1
            except (FileNotFoundError,PermissionError) as e:
                Directory.initialisation_exceptions.append(e)


    def __str__(self):
        pass

    def get_files(self) -> dict[str, File]:
        return(self.files)

    def get_directories(self):
        return(self.directories)

    def get_directories_recursive(self):

        for item in self.path.iterdir():
            if item.is_file():
                continue
            elif item.is_dir():
                continue

