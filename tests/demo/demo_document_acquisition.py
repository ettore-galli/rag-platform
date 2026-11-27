from pathlib import Path

from rag_platform.comproot import rag_loader

BlockType = tuple[float, float, float, float, str, int, int]


def try_rag_loader():
    rag_loader.load_document_corpus(root_directory=Path("/documents-root/"))


if __name__ == "__main__":
    try_rag_loader()
