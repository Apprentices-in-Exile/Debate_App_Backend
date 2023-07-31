from sqlalchemy import Integer, Date
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from session import Base


class Upvote(Base):
    __tablename__ = 'upvotes'

    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.id'))
    conversationID = Column(Integer, ForeignKey('conversations.id'))
    personaID = Column(Integer, ForeignKey('personas.id'))
    createdDate = Column(Date)
    

    def __init__(self, userID, conversationID, personaID, createdDate):
        self.userID = userID
        self.conversationID = conversationID
        self.personaID = personaID
        self.createdDate = createdDate


