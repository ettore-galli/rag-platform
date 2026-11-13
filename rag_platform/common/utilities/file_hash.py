import hashlib
from abc import ABC, abstractmethod
from pathlib import Path


class FileHashCalculatorBase(ABC):
    @abstractmethod
    def get_file_hash(self, file_path: Path, algo: str = "blake2b") -> str: ...


class FileHashCalculator(FileHashCalculatorBase):
    def get_file_hash(self, file_path: Path, algo: str = "blake2b") -> str:
        h = hashlib.new(algo)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
