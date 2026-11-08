from pathlib import Path

from rag_platform.common.base_types import RagCorpusFileTypes
from rag_platform.common.configuration.rag_configuration import (
    RagConfiguration,
    get_rag_configuration,
)
from rag_platform.common.database.database import get_postgres_session
from rag_platform.model_client.ollama_model import OllamaModelClient
from rag_platform.repo.text_embedding import TextEmbeddingRepo
from rag_platform.service.rag_loader.rag_loader import RagLoader
from rag_platform.text_extraction.common import BaseTextExtractor
from rag_platform.text_extraction.pdf_text_extractor import PdfTextExtractor

configuration: RagConfiguration = get_rag_configuration()

ollama_model_client = OllamaModelClient(configuration=configuration)

db_conection = get_postgres_session(configuration=configuration)

text_embedding_repo = TextEmbeddingRepo(session=db_conection)

pdf_text_extractor: BaseTextExtractor = PdfTextExtractor(configuration=configuration)

rag_loader = RagLoader(
    configuration=configuration,
    root_directory=Path("/documents-root/arduino"),
    file_types={RagCorpusFileTypes.PDF},
    text_extractors_map={RagCorpusFileTypes.PDF: pdf_text_extractor},
    embed_model_client=ollama_model_client,
    text_embedding_repo=text_embedding_repo,
    logger=None,
)
