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
def retrieve_data(body):
    # Initialize SQLAlchemy engine if it's not already initialized
    global engine
    if engine is None:
        db_url = get_db_url()
        engine = create_engine(db_url)

    # Retrieve a Conversation object from the database
    with Session(engine) as session:
        conversation_id = body.get('id')
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()

        if conversation is None:
            return {
                'statusCode': 404,
                'body': f'Conversation with ID {conversation_id} not found.'
            }

        return conversation
    

@app.get("/retrieve")
def handle_retrieve(event, context):
    body = json.loads(event.get('body', '{}'))
    # ... Retrieve data from the database ...

    return {"statusCode": 200, "body": json.dumps({"data": data})}