import json 
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.conversations import Conversation 
from sqlalchemy import create_engine
from models.conversations import Conversation 
from database_credentials import get_db_url
from globals import tracer, logger, metrics
from globals import app
from globals import engine


@tracer.capture_method
def store_data(body):
    # Initialize SQLAlchemy engine if it's not already initialized
    global engine
    if engine is None:
        db_url = get_db_url()
        engine = create_engine(db_url)

    # Create a new Conversation object
    conversation = Conversation(body=body.get('body'),
                                title=body.get('title'),
                                isPublic=body.get('isPublic'),
                                createdDate=body.get('createdDate'),
                                userID=body.get('userID'),
                                topicID=body.get('topicID'))

    # Store the Conversation object in the database
    with Session(engine) as session:
        session.add(conversation)
        session.commit()

@app.post("/store")
def handle_store(event, context):
    body = json.loads(event.get('body', '{}'))
    store_data(body)
    return {"statusCode": 200, "body": "Data stored successfully!"}