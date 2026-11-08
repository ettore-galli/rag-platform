from abc import abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any

from ollama import ChatResponse, Client, EmbedResponse, Message

from rag_platform.common.configuration.rag_configuration import RagConfiguration


class BaseModelClient:
    def __init__(self, configuration: RagConfiguration):
        super().__init__()
        self.configuration = configuration
        self.client: Client = Client(host=self.configuration.ollama_configuration.host)

    @abstractmethod
    def embed(self, input: str | Sequence[str] = "") -> EmbedResponse: ...

    @abstractmethod
    def chat(
        self,
        messages: Sequence[Mapping[str, Any] | Message] | None = None,
    ) -> ChatResponse: ...
