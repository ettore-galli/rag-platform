from collections.abc import Iterable
from pathlib import Path

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.repo.text_embedding import TextEmbeddingRepo
from rag_platform.text_extraction.common import BaseTextExtractor

TextExtractorsMap = dict[RagCorpusFileTypes, BaseTextExtractor]


class RagLoader:

    def __init__(
        self,
        root_directory: Path,
        file_types: set[RagCorpusFileTypes],
        text_extractors_map: TextExtractorsMap,
        text_embedding_repo: TextEmbeddingRepo,
    ) -> None:
        self.root_directory: Path = root_directory
        self.file_types: set[RagCorpusFileTypes] = file_types
        self.text_extractors_map: TextExtractorsMap = text_extractors_map
        self.text_embedding_repo: TextEmbeddingRepo = text_embedding_repo

    @staticmethod
    def list_document_files(
        root_directory: Path, file_types: set[RagCorpusFileTypes]
    ) -> Iterable[Path]:
        extensions = {file_type.value.lower() for file_type in file_types}

        return (
            path
            for path in root_directory.rglob("*")
            if path.is_file() and path.suffix.lower() in extensions
        )

    def load_document_corpus(self) -> None:
        pass
