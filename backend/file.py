from __future__ import annotations

from pathlib import Path
import xxhash

CHUNK_SIZE = 1024 * 1024 # 1 MB

class File:
    def __init__(self, file_path: Path):
        self.path: Path = file_path
        self.name: str = file_path.name
        self.size: int = self.path.stat().st_size
        self.hash: int = None

    def __hash__(self) -> int:
        if self.hash:
            # return cached hash
            return self.hash
        
        hasher = xxhash.xxh3_64()

        # Read 1 MB chunks into digest
        with open(self.path, "rb") as file:
            while buffer := file.read(CHUNK_SIZE):
                hasher.update(buffer)

        self.hash = hasher.intdigest()

        return hasher.intdigest()


    def __eq__(self, other: object) -> bool:
        if not (isinstance(other, File)):
            return NotImplemented

        # Check size before checking or calculating hash
        if self.size != other.size:
            return False

        # Check if self and other have hash value
        if not self.hash:
            hash(self)
        if not other.hash:
            hash(other)

        if self.hash == other.hash:
            return True
        return False