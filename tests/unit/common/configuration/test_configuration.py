from rag_platform.common.configuration.rag_configuration import (
    OllamaConfiguration,
    get_rag_configuration,
)


def test_rag_configuration_behaves_ad_dict(mock_environment_variables):
    cfg = get_rag_configuration(prefix="TST")
    assert isinstance(cfg["ollama_configuration"], OllamaConfiguration)


def test_rag_configuration_gets_values_from_environment(mock_environment_variables):
    cfg = get_rag_configuration(prefix="TST")
    assert cfg.ollama_configuration.host == "http://test-host:11434"
    assert cfg.embed_configuration.model == "my-embed-model"
    assert cfg.chat_configuration.model == "my-chat-model"
