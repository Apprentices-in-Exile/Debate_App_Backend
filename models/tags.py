from sqlalchemy import Column
from sqlalchemy import Integer, String
from session import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tagName = Column(String(100), index=True)

    def __init__(self, tagName):
        self.tagName = tagName

    def to_dict(self):
            return {column.name: getattr(self, column.name) for column in self.__table__.columns}
