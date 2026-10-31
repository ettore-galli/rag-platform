from sqlalchemy.orm import Query
from tests.unit.repo.base import BaseRepo

from rag_platform.db_models.text_embeddings import TextEmbedding


class TextEmbeddingRepo(BaseRepo):
    DEFAULT_QUERY_LIMIT: int = 5
    VECTOR_DISTANCE_LABEL: str = "distance"

    def insert_embeddings(
        self, embeddings: list[list[float]], contents: list[str], file_names: list[str]
    ):
        for embedding, content, file_name in zip(
            embeddings, contents, file_names, strict=True
        ):
            new_embedding = TextEmbedding(
                embedding=embedding, content=content, file_name=file_name
            )
            self.session.add(new_embedding)
        self.session.commit()

    def get_similar_embeddings_query(
        self, query_embedding: list[float], limit: int
    ) -> Query[TextEmbedding]:
        return (
            self.session.query(
                TextEmbedding.id,
                TextEmbedding.sentence_number,
                TextEmbedding.content,
                TextEmbedding.file_name,
                TextEmbedding.embedding.cosine_distance(query_embedding).label(
                    TextEmbeddingRepo.VECTOR_DISTANCE_LABEL
                ),
            )
            .order_by(TextEmbeddingRepo.VECTOR_DISTANCE_LABEL)
            .limit(limit)
        )

    def get_similar_embeddings(
        self, query_embedding: list[float], limit: int = DEFAULT_QUERY_LIMIT
    ):
        return self.get_similar_embeddings_query(
            query_embedding=query_embedding, limit=limit
        )
