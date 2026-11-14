from pathlib import Path

from rag_platform.comproot import rag_search

BASE_DIR = Path(__file__).resolve().parent

EXAMPLE_PDF_LOGARITMI = BASE_DIR / "data" / "logaritmi.PDF"

BlockType = tuple[float, float, float, float, str, int, int]


def query_documents(query: str) -> str:
    result = rag_search.search(query=query)
    return str(result)
