from pathlib import Path

from rag_platform.common.base_types import RagCorpusFileTypes
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


def test_load_document_corpus():
    pass
