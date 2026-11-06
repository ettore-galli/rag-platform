from pathlib import Path
from typing import cast

import pymupdf
from pymupdf import Document, Page

from rag_platform.text_extraction.common import (
    BaseTextExtractor,
    DocumentExtractionResult,
    DocumentSourceIdentifier,
)

BlockType = tuple[float, float, float, float, str, int, int]


class PdfTextExtractor(BaseTextExtractor):

    def extract_text_content(
        self, document_source_identifier: DocumentSourceIdentifier
    ) -> DocumentExtractionResult:

        source: Path = Path(document_source_identifier)

        document_content: DocumentExtractionResult = {}
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
