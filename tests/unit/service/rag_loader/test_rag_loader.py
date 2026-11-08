from collections.abc import Sequence
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from ollama import EmbedResponse

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.common.configuration.rag_configuration import get_rag_configuration
from rag_platform.service.rag_loader.rag_loader import RagLoader

BASE_DIR = Path(__file__).resolve().parent

DOCUMENT_ROOT = BASE_DIR / "data" / "documents"


def test_list_document_files():
    files_list: list[Path] = list(
        RagLoader.list_document_files(
            root_directory=DOCUMENT_ROOT,
            file_types={RagCorpusFileTypes.PDF, RagCorpusFileTypes.TXT},
        )
    )
    assert [str(path) for path in list(files_list)] == [
        "/workspace/tests/unit/service/rag_loader/data/documents/doc2.pdf",
        "/workspace/tests/unit/service/rag_loader/data/documents/doc1.pdf",
        "/workspace/tests/unit/service/rag_loader/data/documents/sub1/doc3.pdf",
        "/workspace/tests/unit/service/rag_loader/data/documents/sub1/doc4.txt",
    ]


def test_infer_file_type():
    files_list: list[Path] = list(
        RagLoader.list_document_files(
            root_directory=DOCUMENT_ROOT,
            file_types={RagCorpusFileTypes.PDF, RagCorpusFileTypes.TXT},
        )
    )
    assert [RagLoader.infer_file_type(path) for path in list(files_list)] == [
        RagCorpusFileTypes.PDF,
        RagCorpusFileTypes.PDF,
        RagCorpusFileTypes.PDF,
        RagCorpusFileTypes.TXT,
    ]


def test_load_document_corpus(
    mock_environment_variables: pytest.MonkeyPatch,
):
    cfg = get_rag_configuration(prefix="TST")

    document = Path("example.pdf")

    text_extractor = MagicMock()

    text_extractor.extract_text_content.return_value = {
        (1, 1): "testo uno",
        (1, 2): "testo due",
        (1, 3): "testo tre",
    }

    embed_model_client = MagicMock()

    embed_response = MagicMock(spec=EmbedResponse)
    embed_response.embeddings = [[0.1, 0.2, 0.3]]

    def dummy_embed(input: str | Sequence[str] = "") -> EmbedResponse:
        _ = input
        return EmbedResponse(embeddings=[[0.1, 0.2, 0.3]])

    embed_model_client.embed.side_effect = dummy_embed

    text_embedding_repo = MagicMock()

    loader = RagLoader(
        configuration=cfg,
        root_directory=Path("/dummy"),
        file_types={RagCorpusFileTypes.PDF},
        text_extractors_map={
            RagCorpusFileTypes.PDF: text_extractor,
        },
        embed_model_client=embed_model_client,
        text_embedding_repo=text_embedding_repo,
    )

    with patch.object(
        RagLoader,
        "list_document_files",
        return_value=[document],
    ):

        loader.load_document_corpus()

    text_extractor.extract_text_content.assert_called_once_with(
        document_source_identifier=document
    )

    assert embed_model_client.embed.call_count == 3

    embed_model_client.embed.assert_has_calls(
        [
            call(input="testo uno"),
            call(input="testo due"),
            call(input="testo tre"),
        ]
    )

    assert [c.kwargs["input"] for c in embed_model_client.embed.call_args_list] == [
        "testo uno",
        "testo due",
        "testo tre",
    ]

    assert text_embedding_repo.insert_embeddings.call_count == 1

    text_embedding_repo.insert_embeddings.assert_has_calls(
        [
            call(
                embeddings=[[0.1, 0.2, 0.3], [0.1, 0.2, 0.3], [0.1, 0.2, 0.3]],
                contents=["testo uno", "testo due", "testo tre"],
                file_names=["example.pdf", "example.pdf", "example.pdf"],
            )
        ]
    )
