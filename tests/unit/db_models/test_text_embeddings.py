from rag_platform.db_models.text_embeddings import TextEmbedding


def test_text_embedding_model_behaviour():
    instance = TextEmbedding(
        id=1,
        embedding=[1, 2, 3],
        content="content",
        file_name="filename",
        sentence_number=1,
    )

    assert instance.id == 1
    assert instance.embedding == [1, 2, 3]
    assert instance.content == "content"
    assert instance.file_name == "filename"
    assert instance.sentence_number == 1
