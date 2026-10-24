from rag_platform.common.configuration.config import OllamaConfiguration, get_config


def test_config_basic_behaviour():
    cfg = get_config()
    assert isinstance(cfg["ollama_configuration"], OllamaConfiguration)
