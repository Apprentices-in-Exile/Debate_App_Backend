import json 
# from aws_lambda_powertools.utilities.validation import validate

from models.conversations import Conversation 
from globals import tracer
from globals import app
from globals import engine
from session import session as Session
from session import mysql_engine
# from schemas.conversation import conversation as conversation_schema


@tracer.capture_method
def store_data(body):
    # Initialize SQLAlchemy engine if it's not already initialized
    global engine
    if engine is None:
        engine = mysql_engine

    # Create a new Conversation object
    conversation = Conversation(s3_bucket=body.get('s3_bucket'),
                                s3_key=body.get('s3_key'),
                                title=body.get('title'),
                                isPublic=body.get('isPublic'),
                                createdDate=body.get('createdDate'),
                                userID=body.get('userID'),
                                topicID=body.get('topicID'))

    # Store the Conversation object in the database
    with Session(engine) as session:
        session.add(conversation)
        session.commit()

# @validate(inbound_schema=conversation_schema)
@app.post("/store")
def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    store_data(body)
    return {"statusCode": 200, "body": "Data stored successfully!"}