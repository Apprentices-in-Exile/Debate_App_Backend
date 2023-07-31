from sqlalchemy import String, Integer, Date
from sqlalchemy import Column

from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from session import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userName = Column(String(100), index=True)
    firstName = Column(String(100), index=True)
    lastName = Column(String(100), index=True)
    email = Column(String(100), index=True)
    createdDate = Column(Date)
    conversation = relationship("Conversation", backref=backref("users"))
    persona = relationship("Persona", backref=backref("users"))
    upvote = relationship("Upvote", backref=backref("users"))



    def __init__(self, userName, firstName, lastName, email, createdDate):
        self.userName = userName
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.createdDate = createdDate