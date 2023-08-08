from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database_credentials import get_db_url

database_credentials = get_db_url()
mysql_engine = create_engine(database_credentials)


Session = sessionmaker(bind=mysql_engine)
session = Session()


Base = declarative_base()

from models.conversations import Conversation
from models.personas import Persona
from models.tags import Tag
from models.topics import Topic
from models.upvotes import Upvote
from models.users import User

Base.metadata.create_all(mysql_engine)