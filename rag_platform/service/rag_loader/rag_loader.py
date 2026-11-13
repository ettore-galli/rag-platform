import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Any, cast

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.common.configuration.rag_configuration import RagConfiguration
from rag_platform.model_client.base import BaseModelClient
from rag_platform.repo.text_embedding import TextEmbeddingRepo
from rag_platform.text_extraction.common import (
    BaseTextExtractor,
    DocumentExtractionResult,
)
from rag_platform.text_extraction.null_extractor import NullTextExtractor

TextExtractorsMap = dict[RagCorpusFileTypes, BaseTextExtractor]


class RagLoader:

    def __init__(
        self,
        configuration: RagConfiguration,
        root_directory: Path | None,
        file_types: set[RagCorpusFileTypes],
        text_extractors_map: TextExtractorsMap,
        embed_model_client: BaseModelClient,
        text_embedding_repo: TextEmbeddingRepo,
        logger: logging.Logger | None = None,
    ) -> None:
        self.configuration: RagConfiguration = configuration
        self.root_directory: Path = root_directory or Path(
            configuration.document_corpus.root_directory
        )
        self.file_types: set[RagCorpusFileTypes] = file_types
        self.text_extractors_map: TextExtractorsMap = text_extractors_map
        self.embed_model_client: BaseModelClient = embed_model_client
        self.text_embedding_repo: TextEmbeddingRepo = text_embedding_repo

        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def infer_file_type(file_path: Path) -> RagCorpusFileTypes:
        try:
            return RagCorpusFileTypes(file_path.suffix.lower())
        except ValueError:
            return RagCorpusFileTypes.UNKNOWN

    @staticmethod
    def list_document_files(
        root_directory: Path, file_types: set[RagCorpusFileTypes]
    ) -> Iterable[Path]:

        return (
            path
            for path in root_directory.rglob("*")
            if path.is_file() and RagLoader.infer_file_type(path) in file_types
        )

    def load_document_corpus(self) -> None:
        for document in self.list_document_files(
            root_directory=self.root_directory, file_types=self.file_types
        ):

            text_extractor: BaseTextExtractor = self.text_extractors_map.get(
                RagLoader.infer_file_type(document),
                NullTextExtractor(configuration=self.configuration),
            )

            document_text: DocumentExtractionResult = (
                text_extractor.extract_text_content(document_source_identifier=document)
            )

            embeddings: list[list[float]] = []
            contents: list[Any] = []
            file_names: list[str] = []
            file_hashes: list[str] = []

            for text in document_text.values():
                text_embeddings = self.embed_model_client.embed(input=text)

                if len(text_embeddings.embeddings) == 1:
                    embeddings.extend(
                        cast("list[list[float]]", text_embeddings.embeddings)
                    )
                    contents.append(text)
                    file_names.append(document.name)
                    file_hash = f"<{document.name}>"
                    file_hashes.append(file_hash)

            self.text_embedding_repo.insert_embeddings(
                embeddings=embeddings,
                contents=contents,
                file_names=file_names,
                file_hashes=file_hashes,
            )
