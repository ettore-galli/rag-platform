from typing import Any

from sqlalchemy.orm import Query, Session, scoped_session

from rag_platform.common.database.database import get_postgres_session_from_url

POSTGRES_FIGURATIVE_SESSION_URL = "postgresql+psycopg://"


def get_figurative_session() -> scoped_session[Session]:
    return get_postgres_session_from_url(
        postgres_db_url=POSTGRES_FIGURATIVE_SESSION_URL
    )


def render_query(query: Query[Any]) -> str:
    return str(query.statement.compile(compile_kwargs={"literal_binds": True}))
