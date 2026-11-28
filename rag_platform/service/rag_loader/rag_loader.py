import logging
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import batched
from pathlib import Path
from typing import Any, cast

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.common.configuration.rag_configuration import RagConfiguration
from rag_platform.common.utilities.file_hash import FileHashCalculatorBase
from rag_platform.common.utilities.screen import draw
from rag_platform.model_client.base import BaseModelClient
from rag_platform.repo.text_embedding import TextEmbeddingRepo
from rag_platform.text_extraction.common import (
    BaseTextExtractor,
    DocumentExtractionResult,
)
from rag_platform.text_extraction.null_extractor import NullTextExtractor

TextExtractorsMap = dict[RagCorpusFileTypes, BaseTextExtractor]


@dataclass
class RagLoaderProcessStatus:
    file_name: str | None = None
    total_files: int = 0
    current_file: int = 0
    file_process_step: str | None = None
    file_total_sentences: int = 0
    file_current_sentence: int = 0

    WIDTH = 79

    @staticmethod
    def _progress_bar(current: int, total: int, width: int) -> str:
        if total <= 0:
            return "[" + ("-" * width) + "]"

        ratio = min(max(current / total, 0.0), 1.0)
        percent = round(100 * ratio, 3)
        filled = round(ratio * width)

        return (
            "["
            + str(percent).rjust(6)
            + "%]"
            + "["
            + ("#" * filled)
            + ("-" * (width - filled))
            + "]"
        )

    def render(self) -> list[str]:
        file_bar = self._progress_bar(
            self.current_file,
            self.total_files,
            20,
        )

        sentence_bar = self._progress_bar(
            self.file_current_sentence,
            self.file_total_sentences,
            20,
        )

        row1 = f"File {file_bar} " f"Sentence {sentence_bar}"

        row2 = (
            f"Operazione: {self.file_process_step or '-'} "
            f"File: {self.file_name or '-'}"
        )

        return [
            row1[: self.WIDTH].ljust(self.WIDTH),
            row2[: self.WIDTH].ljust(self.WIDTH),
        ]

    def __str__(self) -> str:
        return "\n".join(self.render())


class RagLoaderBase:
    @staticmethod
    def show_load_progress(status: RagLoaderProcessStatus) -> None:
        draw(status.render())


class RagLoader(RagLoaderBase):

    def __init__(
        self,
        configuration: RagConfiguration,
        root_directory: Path | None,
        file_types: set[RagCorpusFileTypes],
        text_extractors_map: TextExtractorsMap,
        embed_model_client: BaseModelClient,
        text_embedding_repo: TextEmbeddingRepo,
        file_hash_calculator: FileHashCalculatorBase,
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

        self.file_hash_calculator: FileHashCalculatorBase = file_hash_calculator

        self.logger = logger or logging.getLogger(__name__)

        self.batch_size: int = 50

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

    def load_document_corpus(self, root_directory: Path) -> None:

        document_files_list: list[Path] = list(
            self.list_document_files(
                root_directory=root_directory, file_types=self.file_types
            )
        )

        total_files: int = len(document_files_list)

        for document_index, document in enumerate(document_files_list):
            current_file: int = document_index + 1

            self.show_load_progress(
                status=RagLoaderProcessStatus(
                    file_name=str(document),
                    total_files=total_files,
                    current_file=current_file,
                    file_process_step="START",
                )
            )

            file_hash = self.file_hash_calculator.get_file_hash(file_path=document)

            if self.text_embedding_repo.is_file_already_acquired(file_hash=file_hash):
                self.show_load_progress(
                    status=RagLoaderProcessStatus(
                        file_name=str(document),
                        total_files=total_files,
                        current_file=current_file,
                        file_process_step="FILE ALREADY ACQUIRED / SKIPPED",
                    )
                )
                continue

            text_extractor: BaseTextExtractor = self.text_extractors_map.get(
                RagLoader.infer_file_type(document),
                NullTextExtractor(configuration=self.configuration),
            )

            document_text: DocumentExtractionResult = (
                text_extractor.extract_text_content(document_source_identifier=document)
            )

            self.show_load_progress(
                status=RagLoaderProcessStatus(
                    file_name=str(document),
                    total_files=total_files,
                    current_file=current_file,
                    file_process_step="CONTENT READ",
                )
            )

            embeddings: list[list[float]] = []
            contents: list[Any] = []
            file_names: list[str] = []
            file_hashes: list[str] = []

            file_total_sentences: int = len(document_text.values())
            sentence_counter: int = 0

            for batch in batched(document_text.values(), self.batch_size):

                text_embeddings = self.embed_model_client.embed(input=batch)

                if len(text_embeddings.embeddings) == len(batch):

                    embeddings.extend(
                        cast("list[list[float]]", text_embeddings.embeddings)
                    )
                    contents.extend(batch)
                    file_names.extend([document.name] * len(batch))

                    file_hashes.extend([file_hash] * len(batch))

                sentence_counter += len(batch)

                self.show_load_progress(
                    status=RagLoaderProcessStatus(
                        file_name=str(document),
                        total_files=total_files,
                        current_file=current_file,
                        file_process_step="EMBEDDED ITEM",
                        file_total_sentences=file_total_sentences,
                        file_current_sentence=sentence_counter,
                    )
                )
            self.text_embedding_repo.insert_embeddings(
                embeddings=embeddings,
                contents=contents,
                file_names=file_names,
                file_hashes=file_hashes,
            )

            self.show_load_progress(
                status=RagLoaderProcessStatus(
                    file_name=str(document),
                    total_files=total_files,
                    current_file=current_file,
                    file_process_step="EMBEDDING DB INSERT",
                    file_total_sentences=file_total_sentences,
                    file_current_sentence=file_total_sentences,
                )
            )
