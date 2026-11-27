import logging
from typing import TYPE_CHECKING, cast

from rag_platform.db_models.text_embeddings import TextEmbeddingDTO

if TYPE_CHECKING:
    from ollama import EmbedResponse

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.common.configuration.rag_configuration import RagConfiguration
from rag_platform.model_client.base import BaseModelClient
from rag_platform.repo.text_embedding import (
    TextEmbeddingRepo,
    TextEmbeddingSearchResult,
)
from rag_platform.text_extraction.common import (
    BaseTextExtractor,
)

type TextExtractorsMap = dict[RagCorpusFileTypes, BaseTextExtractor]

type RagSearchAnswer = list[TextEmbeddingDTO]
class RagSearch:

    def __init__(
        self,
        configuration: RagConfiguration,
        embed_model_client: BaseModelClient,
        text_embedding_repo: TextEmbeddingRepo,
        logger: logging.Logger | None = None,
    ) -> None:
        self.configuration: RagConfiguration = configuration
        self.embed_model_client: BaseModelClient = embed_model_client
        self.text_embedding_repo: TextEmbeddingRepo = text_embedding_repo

        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def get_merged_search_results(
        search_results: TextEmbeddingSearchResult,
    ) -> TextEmbeddingSearchResult:
        records_map = {
            (item.file_hash, item.sentence_number): item for item in search_results
        }
        return [records_map[key] for key in sorted(records_map.keys())]

    def search(self, query: str) -> RagSearchAnswer:

        query_embeddings: EmbedResponse = self.embed_model_client.embed(input=query)

        search_results = [
            list(
                self.text_embedding_repo.get_similar_embeddings(
                    query_embedding=embedding
                )
            )
            for embedding in cast("list[list[float]]", query_embeddings.embeddings)
        ]

        return RagSearch.get_merged_search_results(
            [item for result in search_results for item in result]
        )

    @staticmethod
    def extract_ui_readable_answer(rag_search_result:RagSearchAnswer, sentence_separator:str="\n")-> str:
        return sentence_separator.join([
            item.content for item in rag_search_result
        ])