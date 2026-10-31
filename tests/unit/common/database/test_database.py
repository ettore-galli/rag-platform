import pytest

from rag_platform.common.configuration.rag_configuration import (
    get_rag_configuration,
)
from rag_platform.common.database.database import get_postgres_connection_string


def test_get_postgres_connection_string(mock_environment_variables: pytest.MonkeyPatch):
    cfg = get_rag_configuration(prefix="TST")
    assert (
        get_postgres_connection_string(configuration=cfg)
        == "postgresql://rag-user:rag-password@my-postgres-host/rag"
    )
