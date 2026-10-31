from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from rag_platform.common.configuration.rag_configuration import RagConfiguration


def get_postgres_connection_string(configuration: RagConfiguration) -> str:
    return (
        f"postgresql://{configuration.vector_db_configuration.postgres_user}:"
        f"{configuration.vector_db_configuration.postgres_password}@"
        f"{configuration.vector_db_configuration.postgres_host}/"
        f"{configuration.vector_db_configuration.postgres_db}"
    )


def get_postgres_session_from_url(postgres_db_url: str) -> scoped_session[Session]:

    engine = create_engine(url=postgres_db_url)

    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def get_postgres_session(configuration: RagConfiguration) -> scoped_session[Session]:

    return get_postgres_session_from_url(
        postgres_db_url=get_postgres_connection_string(configuration=configuration)
    )
