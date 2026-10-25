from rag_platform.common.configuration.rag_configuration import (
    RagConfiguration,
    get_rag_configuration,
)
from rag_platform.common.database.database import get_postgres_session
from rag_platform.model_client.ollama_model import OllamaModelClient

configuration: RagConfiguration = get_rag_configuration()

ollama_model_client = OllamaModelClient(configuration=configuration)

db_conection = get_postgres_session(configuration=configuration)
