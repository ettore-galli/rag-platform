from unittest.mock import ANY, MagicMock, call

import pytest
from ollama import EmbedResponse

from rag_platform.common.configuration.rag_configuration import get_rag_configuration
from rag_platform.db_models.text_embeddings import TextEmbeddingDTO
from rag_platform.service.rag_search.rag_search import RagSearch


def test_search(
    mock_environment_variables: pytest.MonkeyPatch,
):
    cfg = get_rag_configuration(prefix="TST")

    embed_model_client = MagicMock()
    text_embedding_repo = MagicMock()

    embed_model_client.embed.return_value = EmbedResponse(
        embeddings=[
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]
    )

    dto_1 = TextEmbeddingDTO(
        id=1,
        embedding=[1.0, 2.0, 3.0],
        content="The quick brown fox",
        file_name="Fox stories",
        file_hash="123123123",
        sentence_number=65,
        distance=0.1,
    )

    dto_2 = TextEmbeddingDTO(
        id=2,
        embedding=[4.0, 5.0, 6.0],
        content="Jumps over the lazy dog",
        file_name="Fox stories",
        file_hash="123123123",
        sentence_number=66,
        distance=0.2,
    )

    dto_3 = TextEmbeddingDTO(
        id=3,
        embedding=[7.0, 8.0, 9.0],
        content="Lorem ipsum dolor sit amet",
        file_name="Lorem.txt",
        file_hash="456456456",
        sentence_number=1,
        distance=0.3,
    )

    text_embedding_repo.get_similar_embeddings.side_effect = [
        [dto_1, dto_2],
        [dto_3],
    ]

    rag_search = RagSearch(
        configuration=cfg,
        embed_model_client=embed_model_client,
        text_embedding_repo=text_embedding_repo,
    )

    results = rag_search.search("mia query")

    embed_model_client.embed.assert_called_once_with(input="mia query")

    assert text_embedding_repo.get_similar_embeddings.call_count == 2

    text_embedding_repo.get_similar_embeddings.assert_has_calls(
        [
            call(query_embedding=[0.1, 0.2, 0.3]),
            call(query_embedding=[0.4, 0.5, 0.6]),
        ]
    )

    assert results == [
        dto_1,
        dto_2,
        dto_3,
    ]

    assert len(results) == 3

    assert all(isinstance(item, TextEmbeddingDTO) for item in results)

    assert [item.id for item in results] == [1, 2, 3]


def test_get_merged_search_results():
    group_window_size = 5
    example_search_results_data = [
        [
            (
                document,
                sentence,
                f"Example content sentence number {sentence} in document: {document}",
            )
            for sentence in range(
                result_sentence_number - group_window_size,
                result_sentence_number + group_window_size,
            )
        ]
        for document, result_sentence_number in [
            ("file-1", 6),
            #
            ("file-1", 8),
            #
            ("file-1", 21),
            #
            ("file-2", 8),
            ("file-2", 33),
        ]
    ]

    example_search_results = [
        TextEmbeddingDTO(
            id=ANY,
            embedding=ANY,
            content=content,
            file_name=document,
            file_hash=document,
            sentence_number=sentence_number,
            distance=ANY,
        )
        for group in example_search_results_data
        for document, sentence_number, content in group
    ]

    expected_merged_keys = [
        ("file-1", 1),
        ("file-1", 2),
        ("file-1", 3),
        ("file-1", 4),
        ("file-1", 5),
        ("file-1", 6),
        ("file-1", 7),
        ("file-1", 8),
        ("file-1", 9),
        ("file-1", 10),
        ("file-1", 11),
        ("file-1", 12),
        ("file-1", 16),
        ("file-1", 17),
        ("file-1", 18),
        ("file-1", 19),
        ("file-1", 20),
        ("file-1", 21),
        ("file-1", 22),
        ("file-1", 23),
        ("file-1", 24),
        ("file-1", 25),
        ("file-2", 3),
        ("file-2", 4),
        ("file-2", 5),
        ("file-2", 6),
        ("file-2", 7),
        ("file-2", 8),
        ("file-2", 9),
        ("file-2", 10),
        ("file-2", 11),
        ("file-2", 12),
        ("file-2", 28),
        ("file-2", 29),
        ("file-2", 30),
        ("file-2", 31),
        ("file-2", 32),
        ("file-2", 33),
        ("file-2", 34),
        ("file-2", 35),
        ("file-2", 36),
        ("file-2", 37),
    ]

    merged = RagSearch.get_merged_search_results(search_results=example_search_results)

    merged_keys = [(item.file_hash, item.sentence_number) for item in merged]

    assert merged_keys == expected_merged_keys


def test_extract_ui_readable_answer():
    rag_search_result = [
        TextEmbeddingDTO(
            id=ANY,
            embedding=ANY,
            content=content,
            file_name=ANY,
            file_hash=ANY,
            sentence_number=sentence_number,
            distance=ANY,
        )
        for sentence_number, content in [
            (1, "Sentence 1"),
            (2, "Sentence 2"),
            (1, "Sentence 3"),
        ]
    ]

    assert (
        RagSearch.extract_ui_readable_answer(
            rag_search_result=rag_search_result, sentence_separator="*"
        )
        == "Sentence 1*Sentence 2*Sentence 3"
    )
