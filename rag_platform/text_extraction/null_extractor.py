from rag_platform.text_extraction.common import (
    BaseTextExtractor,
    DocumentExtractionResult,
    DocumentSourceIdentifier,
)

BlockType = tuple[float, float, float, float, str, int, int]


class NullTextExtractor(BaseTextExtractor):

    def extract_text_content(
        self, document_source_identifier: DocumentSourceIdentifier
    ) -> DocumentExtractionResult:
        _ = document_source_identifier

        null_document_content: DocumentExtractionResult = {}

        return null_document_content
