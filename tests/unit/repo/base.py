from sqlalchemy.orm import scoped_session


class BaseRepo:
    def __init__(self, session: scoped_session):
        self.session: scoped_session = session
