from abc import abstractmethod
from typing import Any

from rag_platform.common.configuration.rag_configuration import RagConfiguration

DocumentSourceIdentifier = str
DocumentExtractionResult = dict[tuple[int, int], Any]


class BaseTextExtractor:
    def __init__(self, configuration: RagConfiguration):
        super().__init__()
        self.configuration = configuration

    @abstractmethod
    def convert_document(
        self, document_source_identifier: DocumentSourceIdentifier
    ) -> DocumentExtractionResult: ...
