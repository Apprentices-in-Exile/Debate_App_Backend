from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from local_settings import DATABASE_PASSWORD
from local_settings import DATABASE_ENDPOINT
from local_settings import DATABASE_NAME
from local_settings import USERNAME

# create an engine
engine = create_engine(f"mysql://{USERNAME}:{DATABASE_PASSWORD}@{DATABASE_ENDPOINT}/{DATABASE_NAME}", echo=True)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

session = Session()
Base = declarative_base()