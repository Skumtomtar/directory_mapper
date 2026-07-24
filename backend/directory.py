from __future__ import annotations

from pathlib import Path
from collections import defaultdict

from file import File


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

                # If item is a directory, create new Directory object and 
                # add this Directories child directory dictionary
                elif item.is_dir():
                    self.directories[str(item)] = Directory(item)
                    Directory.total_directories += 1
            except (FileNotFoundError,PermissionError) as e:
                Directory.initialisation_exceptions.append(e)

    # NOTE - Review and consider if this needs to be a static method.
    # Refactor to iterative instead of recursive
    @staticmethod
    def get_files_recursive(this_dir: Directory) -> list[File] | None:
        # Add files of current directory to list
        unpacked_files = [file for file in this_dir.files.values()]
        
        # Recursively iterate over each sub directory, recursively adding contained files to list
        for sub_dir in this_dir.directories.values():
            unpacked_files.extend(this_dir.get_files_recursive(sub_dir))
        return unpacked_files


    """
        Approach for comparing files:
        Construct dictionary of files (see Generators?)
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
                        Test if dupe is in set:
                            if so, append dupe to list
                            append(set.file) to list - capture existing dupe using current file as key

                Later:
                    Take second list (second directory).
                    Merge into single list for testing of duplication
                    After list of duplicates has been constructed, split it into
                    two lists, using list.anchor as seperator
    """

    # Duplicates are identified by adding
    # NOTE: Review logic - unique files erroneously flagged
    def find_duplicates(self, file_list: list[File]) -> list[File]:
        file_sizes: dict[int, list[File]] = defaultdict(list) # Default initialise to dict[list]
        candidate_duplicates: list[dict[int, File]] = []
        duplicates_set = set()
        confirmed_duplicates: list[File] = []


        # Iterate over list of files
        # Add each to dict using file size as key
        # Dict keys with multiple files contain candidate duplicates
        for file in file_list:
            file_sizes[file.size].append(file)

        # Construct list of duplicate file dict
        for size in file_sizes:
            if len(file_sizes[size]) > 1:
                candidate_duplicates.extend(file_sizes[size])

        # Hash each duplicate file and test against duplicate set
        for file in candidate_duplicates:
            if file in duplicates_set:
                confirmed_duplicates.append(file)
            else:
                duplicates_set.add(file)

        return confirmed_duplicates