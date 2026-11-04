from pathlib import Path
from typing import Any, cast

import pymupdf
from pymupdf import Document, Page

BASE_DIR = Path(__file__).resolve().parent

EXAMPLE_PDF_LOGARITMI = BASE_DIR / "data" / "logaritmi.PDF"

BlockType = tuple[float, float, float, float, str, int, int]


def convert_doc(source: Path) -> dict[Any, Any]:

    document_content: dict[Any, Any] = {}
    document: Document = pymupdf.open(source)

    page_index: int
    page: Page

    for page_index, page in enumerate(document):  # type: ignore

        blocks: list[BlockType] = cast(
            "list[BlockType]",
            page.get_text("blocks"),  # pyright: ignore[reportUnknownMemberType]
        )

        block: BlockType

        for block in blocks:

            _, _, _, _, content, block_no, block_type = block
            if block_type == 0:
                document_content[(page_index, block_no)] = content.strip()

    return document_content


def try_docling():

    document: Path = EXAMPLE_PDF_LOGARITMI

    converted: dict[Any, Any] = convert_doc(source=document)

    for item in converted.values():
        print(item)


if __name__ == "__main__":
    try_docling()
