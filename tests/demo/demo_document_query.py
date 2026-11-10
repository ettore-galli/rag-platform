from pathlib import Path

from rag_platform.comproot import rag_search

BASE_DIR = Path(__file__).resolve().parent

EXAMPLE_PDF_LOGARITMI = BASE_DIR / "data" / "logaritmi.PDF"

BlockType = tuple[float, float, float, float, str, int, int]


def try_rag_search():
    result = rag_search.search("carrier")
    print(result)


if __name__ == "__main__":
    try_rag_search()
