from sqlalchemy import String, Integer, Date, Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from session import Base

#  Many to Many Mapping Models

conversation_persona = Table(
    'conversation_persona', Base.metadata,
    Column('conversationID', Integer, ForeignKey('conversations.id')),
    Column('personaID', Integer, ForeignKey('personas.id'))
)


conversation_tag = Table(
    'conversation_tag', Base.metadata,
    Column('conversationID', Integer, ForeignKey('conversations.id')),
    Column('tagID', Integer, ForeignKey('tags.id'))
)


#  Conversation Model 

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    s3_bucket = Column(String(100), index=True)
    s3_key = Column(String(100), index=True)
    title = Column(String(100), index=True)
    isPublic = Column(Boolean)
    createdDate = Column(Date)
    userID = Column(Integer, ForeignKey('users.id'))
    topicID = Column(Integer, ForeignKey('topics.id'))
    upvote = relationship("Upvote", backref=backref("conversations"))
    followingPersona = relationship('Persona', secondary=conversation_persona, backref=backref('followers'))
    followingTag = relationship('Tag', secondary=conversation_tag, backref=backref('followers'))

    def __init__(self, s3_bucket, s3_key, title, isPublic, createdDate, userID, topicID):
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.title = title
        self.isPublic = isPublic
        self.createdDate = createdDate
        self.userID = userID
        self.topicID = topicID
