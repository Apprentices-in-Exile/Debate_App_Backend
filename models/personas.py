from sqlalchemy import String, Integer, Date, Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from session import Base


class Persona(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    personaName = Column(String(100), index=True)
    s3_bucket = Column(String(100), index=True)
    s3_key = Column(String(100), index=True)
    details = Column(String(100), index=True)
    isPublic = Column(Boolean)
    createdDate = Column(Date)
    userID = Column(Integer, ForeignKey('users.id'))
    upvote = relationship("Upvote", backref=backref("personas"))

    def __init__(self, personaName, s3_bucket, s3_key, details, isPublic, createdDate, userID):
        self.personaName = personaName
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.details = details
        self.isPublic = isPublic
        self.createdDate = createdDate
        self.userID = userID
        
    
    def to_dict(self):
            data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
            if 'createdDate' in data and data['createdDate']:
                data['createdDate'] = data['createdDate'].isoformat()
            return data