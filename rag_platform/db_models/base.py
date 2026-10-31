from typing import Any

from sqlalchemy.orm import DeclarativeBase


class DbModelBase(DeclarativeBase):
    def to_dict(self) -> dict[str, Any]:
        return {column: getattr(self, column) for column in self.columns()}

    def columns(self) -> list[str]:
        table = getattr(self, "__table__", None)
        if table is not None:
            return list(self.__table__.columns.keys())
        return []
