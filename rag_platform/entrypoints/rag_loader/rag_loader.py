from pathlib import Path

from rag_platform.comproot import rag_loader


def load_documents(root_directory: str) -> None:
    rag_loader.load_document_corpus(root_directory=Path(root_directory))
