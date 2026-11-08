from enum import StrEnum


class RagCorpusFileTypes(StrEnum):
    UNKNOWN = ""
    PDF = ".pdf"
    DOCX = ".docx"
    TXT = ".txt"
    MD = ".md"
