from pathlib import Path

from rag_platform.common.utilities.file_hash import FileHashCalculatorBase


class DummyFileHashCalculator(FileHashCalculatorBase):
    def get_file_hash(self, file_path: Path, algo: str = "blake2b") -> str:
        _ = algo
        return f"<{file_path.name}>"
