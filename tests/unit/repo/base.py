from sqlalchemy.orm import Session, scoped_session


class BaseRepo:
    def __init__(self, session: scoped_session[Session]):
        self.session: scoped_session[Session] = session
