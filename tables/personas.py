from sqlalchemy import String, Integer, Date, Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from session import Base


class Persona(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    personaName = Column(String(100), index=True)
    image = Column(String(100), index=True)
    details = Column(String(100), index=True)
    isPublic = Column(Boolean)
    createdDate = Column(Date)
    userID = Column(Integer, ForeignKey('users.id'))
    upvote = relationship("Upvote", backref=backref("personas"))

    def __init__(self, personaName, image, details, isPublic, createdDate, userID):
        self.personaName = personaName
        self.image = image
        self.details = details
        self.isPublic = isPublic
        self.createdDate = createdDate
        self.userID = userID