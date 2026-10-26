from rag_platform.db_models.text_embeddings import TextEmbedding
from tests.unit.repo.base import BaseRepo


class TextEmbeddingRepo(BaseRepo):

    def insert_embeddings(
        self, embeddings: list[list[float]], contents: list[str], file_names: list[str]
    ):
        for embedding, content, file_name in zip(embeddings, contents, file_names):
            new_embedding = TextEmbedding(
                embedding=embedding, content=content, file_name=file_name
            )
            self.session.add(new_embedding)
        self.session.commit()
