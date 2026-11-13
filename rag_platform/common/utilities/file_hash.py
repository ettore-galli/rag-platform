import hashlib
from pathlib import Path


def get_file_hash(file_path: Path, algo: str = "blake2b"):
    h = hashlib.new(algo)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
