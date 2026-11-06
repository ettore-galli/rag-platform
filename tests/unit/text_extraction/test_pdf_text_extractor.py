from pathlib import Path

import pytest

from rag_platform.common.configuration.rag_configuration import get_rag_configuration
from rag_platform.text_extraction.pdf_text_extractor import PdfTextExtractor

BASE_DIR = Path(__file__).resolve().parent

SAMPLE_1 = BASE_DIR / "data" / "pdf_text_extractor" / "sample-1.pdf"


def test_pdf_text_extractor(
    mock_environment_variables: pytest.MonkeyPatch,
):
    cfg = get_rag_configuration(prefix="TST")

    extractor = PdfTextExtractor(configuration=cfg)

    document_source_identifier: str = str(SAMPLE_1)

    content = extractor.extract_text_content(
        document_source_identifier=document_source_identifier
    )
    assert content[(2, 2)] == (
        '" Mirifici logarithmorum canonis descriptio" del 1614. '
        "\nCon essa egli sperava di fornire uno strumento che "
        "\nrendesse molto più veloci i calcoli degli astronomi. "
        "\nLaplace, 200 anni dopo, riconobbe il successo di questo "
        '\nintendimento, scrivendo che il lavoro di Napier "aveva '
        '\nraddoppiato la vita agli astronomi".'
    )
