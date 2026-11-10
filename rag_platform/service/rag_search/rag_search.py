import logging
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from ollama import EmbedResponse

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.common.configuration.rag_configuration import RagConfiguration
from rag_platform.db_models.text_embeddings import TextEmbedding
from rag_platform.model_client.base import BaseModelClient
from rag_platform.repo.text_embedding import TextEmbeddingRepo
from rag_platform.text_extraction.common import (
    BaseTextExtractor,
)

TextExtractorsMap = dict[RagCorpusFileTypes, BaseTextExtractor]


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

    def search(self, query: str) -> list[TextEmbedding]:

        query_embeddings: EmbedResponse = self.embed_model_client.embed(input=query)

        search_results = [
            list(
                self.text_embedding_repo.get_similar_embeddings(
                    query_embedding=embedding
                )
            )
            for embedding in cast("list[list[float]]", query_embeddings.embeddings)
        ]

        return [item for result in search_results for item in result]
