from dataclasses import dataclass

from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column

from rag_platform.db_models.base import DbModelBase


@dataclass
class TextEmbeddingDTO:
    id: int
    embedding: list[float]
    content: str
    file_name: str
    file_hash: str
    sentence_number: int
    distance: float | None = None


class TextEmbedding(DbModelBase):
    __tablename__ = "text_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    embedding: Mapped[list[float]] = mapped_column(Vector)
    content: Mapped[str] = mapped_column()
    file_name: Mapped[str] = mapped_column(nullable=False)
    file_hash: Mapped[str] = mapped_column(nullable=False)
    sentence_number: Mapped[int] = mapped_column(nullable=False)
