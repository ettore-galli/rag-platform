import pytest


@pytest.fixture(autouse=False)
def mock_environment_variables(monkeypatch):
    for variable, value in [
        (
            "TST_OLLAMA_CONFIGURATION_HOST",
            "http://test-host:11434",
        ),
        (
            "TST_EMBED_CONFIGURATION_MODEL",
            "my-embed-model",
        ),
        (
            "TST_CHAT_CONFIGURATION_MODEL",
            "my-chat-model",
        ),
        (
            "TST_VECTOR_DB_POSTGRES_DB",
            "rag",
        ),
        (
            "TST_VECTOR_DB_POSTGRES_USER",
            "rag-user",
        ),
        (
            "TST_VECTOR_DB_POSTGRES_PASSWORD",
            "rag-password",
        ),
    ]:
        monkeypatch.setenv(variable, value)
