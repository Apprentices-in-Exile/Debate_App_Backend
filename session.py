from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from local_settings import DB_PASSWORD

# create an engine
engine = create_engine(f"mysql://admin:{DB_PASSWORD}@database-1.cj8yik5n6htq.us-east-2.rds.amazonaws.com/test1", echo=True)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

session = Session()
Base = declarative_base()