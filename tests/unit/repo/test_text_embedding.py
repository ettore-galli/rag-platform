from typing import cast
from unittest.mock import Mock

from rag_platform.db_models.text_embeddings import TextEmbedding
from rag_platform.repo.text_embedding import TextEmbeddingRepo


def test_insert_embeddings_adds_all_entities_and_commits():
    session = Mock()

    repo = TextEmbeddingRepo(session=session)
    repo.session = session

    embeddings = [
        [0.1, 0.2],
        [0.3, 0.4],
    ]
    contents = [
        "first sentence",
        "second sentence",
    ]
    file_names = [
        "file1.txt",
        "file2.txt",
    ]

    repo.insert_embeddings(
        embeddings=embeddings,
        contents=contents,
        file_names=file_names,
    )

    assert session.add.call_count == 2

    first_entity = session.add.call_args_list[0].args[0]
    second_entity = session.add.call_args_list[1].args[0]

    assert isinstance(first_entity, TextEmbedding)
    assert first_entity.embedding == [0.1, 0.2]
    assert first_entity.content == "first sentence"
    assert first_entity.file_name == "file1.txt"

    assert isinstance(second_entity, TextEmbedding)
    assert second_entity.embedding == [0.3, 0.4]
    assert second_entity.content == "second sentence"
    assert second_entity.file_name == "file2.txt"

    session.commit.assert_called_once_with()

    add_calls = [
        cast(TextEmbedding, mock_call.args[0]).to_dict()
        for mock_call in session.add.mock_calls
    ]

    assert add_calls == [
        {
            "id": None,
            "embedding": [0.1, 0.2],
            "content": "first sentence",
            "file_name": "file1.txt",
            "sentence_number": None,
        },
        {
            "id": None,
            "embedding": [0.3, 0.4],
            "content": "second sentence",
            "file_name": "file2.txt",
            "sentence_number": None,
        },
    ]
