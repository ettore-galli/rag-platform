from collections.abc import Mapping, Sequence
from typing import Any

from ollama import ChatResponse, Client, EmbedResponse, Message

from rag_platform.common.configuration.rag_configuration import RagConfiguration


class OllamaModelClient:
    def __init__(self, configuration: RagConfiguration):
        super().__init__()
        self.configuration = configuration
        self.client: Client = Client(host=self.configuration.ollama_configuration.host)

    def embed(self, input: str | Sequence[str] = "") -> EmbedResponse:
        return self.client.embed(
            model=self.configuration.embed_configuration.model, input=input
        )

    def chat(
        self,
        messages: Sequence[Mapping[str, Any] | Message] | None = None,
    ) -> ChatResponse:
        return self.client.chat(
            model=self.configuration.chat_configuration.model, messages=messages
        )
