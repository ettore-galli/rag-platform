import os
from dataclasses import dataclass, fields
from typing import ClassVar, get_type_hints

from rag_platform.common.dataclassdict import DataClassDict

DEFAULT_CONFIGURATION_PREFIX: str = "RAG"


def build_dataclass(class_to_build: type, prefix: str):
    values = {}

    type_hints = get_type_hints(class_to_build)

    for field in fields(class_to_build):
        field_type = type_hints[field.name]

        if hasattr(field_type, "ENV_SECTION"):
            values[field.name] = build_dataclass(field_type, prefix)
            continue

        section = class_to_build.ENV_SECTION

        env_name = f"{prefix}_{section}_{field.name}".upper()

        value = os.environ.get(env_name)

        if value is None:
            raise ValueError(f"Environment variable '{env_name}' not defined")

        values[field.name] = value

    return class_to_build(**values)


@dataclass(frozen=True)
class OllamaConfiguration(DataClassDict):
    ENV_SECTION: ClassVar[str] = "OLLAMA_CONFIGURATION"

    host: str


@dataclass(frozen=True)
class EmbedConfiguration(DataClassDict):
    ENV_SECTION: ClassVar[str] = "EMBED_CONFIGURATION"

    model: str


@dataclass(frozen=True)
class ChatConfiguration(DataClassDict):
    ENV_SECTION: ClassVar[str] = "CHAT_CONFIGURATION"

    model: str


@dataclass(frozen=True)
class VectorDbConfiguration(DataClassDict):
    ENV_SECTION: ClassVar[str] = "VECTOR_DB"

    postgres_db: str
    postgres_user: str
    postgres_password: str


@dataclass(frozen=True)
class RagConfiguration(DataClassDict):
    ollama_configuration: OllamaConfiguration
    embed_configuration: EmbedConfiguration
    chat_configuration: ChatConfiguration
    vector_db_configuration: VectorDbConfiguration


def get_rag_configuration(
    prefix: str = DEFAULT_CONFIGURATION_PREFIX,
) -> RagConfiguration:
    return RagConfiguration(
        ollama_configuration=build_dataclass(
            OllamaConfiguration,
            prefix,
        ),
        embed_configuration=build_dataclass(
            EmbedConfiguration,
            prefix,
        ),
        chat_configuration=build_dataclass(
            ChatConfiguration,
            prefix,
        ),
        vector_db_configuration=build_dataclass(
            VectorDbConfiguration,
            prefix,
        ),
    )
