from dataclasses import dataclass

from rag_platform.common.dataclassdict import DataClassDict


@dataclass(frozen=True)
class OllamaConfiguration(DataClassDict):
    host: str


@dataclass(frozen=True)
class Config(DataClassDict):
    ollama_configuration: OllamaConfiguration


def get_ollama_configuration() -> OllamaConfiguration:
    return OllamaConfiguration(
        host="blablabla",
    )


def get_config() -> Config:
    return Config(ollama_configuration=get_ollama_configuration())
