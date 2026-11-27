from sqlalchemy import Row, literal
from sqlalchemy.orm import Query
from tests.unit.repo.base import BaseRepo

from rag_platform.db_models.text_embeddings import (
    TextEmbedding,
    TextEmbeddingDTO,
)

type EmbeddingQueryResult = Row[
    int,
    int,
    list[float],
    str,
    str,
    str,
    float,
]

type TextEmbeddingSearchResult = list[TextEmbeddingDTO]


class TextEmbeddingRepo(BaseRepo):
    DEFAULT_QUERY_LIMIT: int = 5
    VECTOR_DISTANCE_LABEL: str = "distance"

    def is_file_already_acquired_query(self, file_hash: str) -> Query[Row[int]]:
        return self.session.query(TextEmbedding.id).filter(
            TextEmbedding.file_hash == file_hash
        )

    def is_file_already_acquired(self, file_hash: str) -> bool:
        return self.is_file_already_acquired_query(file_hash).first() is not None

    def insert_embeddings(
        self,
        embeddings: list[list[float]],
        contents: list[str],
        file_names: list[str],
        file_hashes: list[str],
    ):
        for index, (embedding, content, file_name, file_hash) in enumerate(
            zip(embeddings, contents, file_names, file_hashes, strict=True)
        ):
            new_embedding = TextEmbedding(
                embedding=embedding,
                content=content,
                file_name=file_name,
                file_hash=file_hash,
                sentence_number=index + 1,
            )
            self.session.add(new_embedding)
        self.session.commit()

    def get_similar_embeddings_query(
        self, query_embedding: list[float], limit: int
    ) -> Query[EmbeddingQueryResult]:
        return (
            self.session.query(
                TextEmbedding.id,
                TextEmbedding.sentence_number,
                TextEmbedding.embedding,
                TextEmbedding.content,
                TextEmbedding.file_name,
                TextEmbedding.file_hash,
                TextEmbedding.embedding.cosine_distance(query_embedding).label(
                    TextEmbeddingRepo.VECTOR_DISTANCE_LABEL
                ),
            )
            .order_by(TextEmbeddingRepo.VECTOR_DISTANCE_LABEL)
            .limit(limit)
        )

    @staticmethod
    def get_dto_from_result(result: EmbeddingQueryResult) -> TextEmbeddingDTO:
        return TextEmbeddingDTO(
            id=result.id,
            embedding=result.embedding,
            content=result.content,
            file_name=result.file_name,
            file_hash=result.file_hash,
            sentence_number=result.sentence_number,
            distance=result.distance,
        )

    def get_similar_embeddings(
        self, query_embedding: list[float], limit: int = DEFAULT_QUERY_LIMIT
    ) -> list[TextEmbeddingDTO]:
        return [
            TextEmbeddingRepo.get_dto_from_result(row)
            for row in self.get_similar_embeddings_query(
                query_embedding=query_embedding, limit=limit
            ).all()
        ]

    def get_surrounding_sentences_query(
        self, base_embedding: TextEmbeddingDTO, group_window_size: int
    ) -> Query[EmbeddingQueryResult]:
        return (
            self.session.query(
                TextEmbedding.id,
                TextEmbedding.sentence_number,
                TextEmbedding.embedding,
                TextEmbedding.content,
                TextEmbedding.file_name,
                TextEmbedding.file_hash,
                literal(0.0).label(TextEmbeddingRepo.VECTOR_DISTANCE_LABEL),
            )
            .filter(TextEmbedding.file_hash == base_embedding.file_hash)
            .filter(
                TextEmbedding.sentence_number
                >= base_embedding.sentence_number - group_window_size
            )
            .filter(
                TextEmbedding.sentence_number
                <= base_embedding.sentence_number + group_window_size
            )
        )

    def get_surrounding_sentences(
        self, base_embedding: TextEmbeddingDTO, group_window_size: int
    ) -> list[TextEmbeddingDTO]:
        return [
            TextEmbeddingRepo.get_dto_from_result(row)
            for row in self.get_surrounding_sentences_query(
                base_embedding=base_embedding, group_window_size=group_window_size
            ).all()
        ]
