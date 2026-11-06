from pathlib import Path
from typing import Any

from rag_platform.comproot import pdf_text_extractor

BASE_DIR = Path(__file__).resolve().parent

EXAMPLE_PDF_LOGARITMI = BASE_DIR / "data" / "logaritmi.PDF"

BlockType = tuple[float, float, float, float, str, int, int]


def try_docling():

    document: Path = EXAMPLE_PDF_LOGARITMI

    converted: dict[Any, Any] = pdf_text_extractor.extract_text_content(
        document_source_identifier=str(document)
    )

    for item in converted.values():
        print(item)


if __name__ == "__main__":
    try_docling()
