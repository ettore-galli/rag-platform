from collections.abc import Mapping, Sequence
from typing import Any

from ollama import ChatResponse, EmbedResponse, Message

from rag_platform.model_client.base import BaseModelClient


class OllamaModelClient(BaseModelClient):
    def embed(self, input: str | Sequence[str] = "") -> EmbedResponse:
        return self.client.embed(
            model=self.configuration.embed_configuration.model, input=input
        )

    def chat(
        self,
        messages: Sequence[Mapping[str, Any] | Message] | None = None,
    ) -> ChatResponse:
        return self.client.chat(  # type: ignore[reportUnknownMemberType]
            model=self.configuration.chat_configuration.model, messages=messages
        )
