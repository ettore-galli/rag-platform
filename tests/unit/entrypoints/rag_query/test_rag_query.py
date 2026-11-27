from unittest.mock import ANY, patch

from rag_platform.db_models.text_embeddings import TextEmbeddingDTO
from rag_platform.entrypoints.rag_query.rag_query import query_documents


def test_query_documents_forwards_query_and_returns_string():
    with patch(
        "rag_platform.entrypoints.rag_query.rag_query.rag_search.search",
        return_value=[
            TextEmbeddingDTO(
                id=ANY,
                embedding=ANY,
                content="risultato",
                file_name=ANY,
                file_hash=ANY,
                sentence_number=ANY,
                distance=ANY,
            )
        ],
    ) as search:
        result = query_documents("domanda")

    search.assert_called_once_with(query="domanda")
    assert result == "risultato"
    assert isinstance(result, str)


def test_query_documents_returns_string_for_empty_results():
    with patch(
        "rag_platform.entrypoints.rag_query.rag_query.rag_search.search",
        return_value=[],
    ):
        assert query_documents("domanda") == ""


def test_query_documents_propagates_service_errors():
    with patch(
        "rag_platform.entrypoints.rag_query.rag_query.rag_search.search",
        side_effect=RuntimeError("search failed"),
    ):
        try:
            query_documents("domanda")
        except RuntimeError as error:
            assert str(error) == "search failed"
        else:
            raise AssertionError("RuntimeError was not propagated")
