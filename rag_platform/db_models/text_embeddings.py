from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column

from rag_platform.db_models.base import DbModelBase


class TextEmbedding(DbModelBase):
    __tablename__ = "text_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    embedding: Mapped[list[float]] = mapped_column(Vector)
    content: Mapped[str] = mapped_column()
    file_name: Mapped[str] = mapped_column()
    sentence_number: Mapped[int | None] = mapped_column(nullable=True)
