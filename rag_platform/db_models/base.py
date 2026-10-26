from sqlalchemy.orm import DeclarativeBase


class DbModelBase(DeclarativeBase):
    def to_dict(self) -> dict:
        return {column: getattr(self, column) for column in self.columns()}

    def columns(self) -> list[str]:
        if self.__table__ is not None:
            return list(self.__table__.columns.keys())
        return []
