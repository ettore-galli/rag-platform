from pathlib import Path

from rag_platform.common.utilities.file_hash import FileHashCalculator

BASE_DIR = Path(__file__).resolve().parent

EXAMPLE_FILE_1 = BASE_DIR / "data" / "example-file-1.txt"


def test_get_file_hash():
    file_hash = FileHashCalculator.get_file_hash(file_path=EXAMPLE_FILE_1)
    assert (
        file_hash
        == "f4e1fb9e9c231b41f84f5dcfc2aec4c21a7a3b552b99f89dfd4073364d3b1dd09e1144c859bf875a39865cf1352e44eb7815a1516af84bca158859e4f0150d79"
    )
