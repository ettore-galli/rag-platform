from rag_platform.common.database.tools import (
    get_figurative_session,
    render_query,
)
from rag_platform.db_models.text_embeddings import TextEmbedding


def test_render_query():
    figurative_session = get_figurative_session()
    assert render_query(
        figurative_session.query(
            TextEmbedding.id,
            TextEmbedding.sentence_number,
            TextEmbedding.content,
            TextEmbedding.file_name,
        )
    ) == (
        "SELECT text_embeddings.id, text_embeddings.sentence_number, text_embeddings.content, text_embeddings.file_name "
        "\nFROM text_embeddings"
    )
