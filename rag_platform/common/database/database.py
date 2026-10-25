from typing import cast

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from rag_platform.common.configuration.rag_configuration import RagConfiguration


def get_postgres_connection_string(configuration: RagConfiguration) -> str:
    return (
        f"postgresql://{configuration.vector_db_configuration.postgres_user}:"
        f"{configuration.vector_db_configuration.postgres_password}@"
        f"{configuration.vector_db_configuration.postgres_host}/"
        f"{configuration.vector_db_configuration.postgres_db}"
    )


def get_postgres_session(configuration: RagConfiguration) -> scoped_session:

    engine = create_engine(
        url=get_postgres_connection_string(configuration=configuration)
    )

    session_factory = sessionmaker(bind=engine)
    return cast(scoped_session, scoped_session(session_factory))
