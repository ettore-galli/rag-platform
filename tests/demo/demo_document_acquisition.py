from pathlib import Path

from rag_platform.comproot import rag_loader

BASE_DIR = Path(__file__).resolve().parent

EXAMPLE_PDF_LOGARITMI = BASE_DIR / "data" / "logaritmi.PDF"

BlockType = tuple[float, float, float, float, str, int, int]


def try_rag_loader():
    rag_loader.load_document_corpus()


if __name__ == "__main__":
    try_rag_loader()
