from pathlib import Path
import xxhash

CHUNK_SIZE = 1024 * 1024 # 1 MB

class File:
    def __init__(self, file_path: Path):
        self.path: Path = file_path
        self.name: str = file_path.name
        self.extension: str = file_path.suffix
        self.size: int = self.path.stat().st_size
        self.hash: int = None

    def hash_self(self):
        hasher = xxhash.xxh3_64
        
        # Read 1 MB chunks into digest
        with open(self.path, "rb") as file:
            while buffer := file.read(CHUNK_SIZE):
                hasher.update(buffer)
        
        self.hash = hasher.intdigest()

    def __eq__(self, other: object) -> bool:
        # Check size before checking or calculating hash
        if self.size != other.size:
            return False
        
        # Check if this and other have hash value
        if not self.hash:
            self.hash_self()
        if not other.hash:
            other.hash_self()

        if self.hash != other.hash:
            return False
        return True
    
    def __hash__(self) -> int:
        return self.hash_self()