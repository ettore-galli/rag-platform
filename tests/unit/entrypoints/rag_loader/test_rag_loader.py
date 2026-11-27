from unittest.mock import patch

from rag_platform.entrypoints.rag_loader.rag_loader import load_documents


def test_load_documents_calls_service():
    with patch(
        "rag_platform.entrypoints.rag_loader.rag_loader."
        "rag_loader.load_document_corpus"
    ) as load_corpus:
        load_documents()

    load_corpus.assert_called_once_with()
