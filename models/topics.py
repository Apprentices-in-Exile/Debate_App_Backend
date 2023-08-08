from sqlalchemy import String, Integer, Date, Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from session import Base


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    topicName = Column(String(100), index=True)
    details = Column(String(100), index=True)
    createdDate = Column(Date)
    conversation = relationship("Conversation", backref=backref("topics"), uselist=False)

    def __init__(self, topicName, details, createdDate):
        self.topicName = topicName
        self.details = details
        self.createdDate = createdDate


    def to_dict(self):
            data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
            if 'createdDate' in data and data['createdDate']:
                data['createdDate'] = data['createdDate'].isoformat()
            return data