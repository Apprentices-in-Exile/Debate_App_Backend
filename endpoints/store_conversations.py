import json 
import boto3
from aws_lambda_powertools.utilities.validation import validate

from models.conversations import Conversation
from models.topics import Topic
from models.users import User
from globals import tracer
from globals import app
from session import session
from s3_key import generate_s3_key
from s3_key import s3_bucket
# from schemas.conversation import conversation as conversation_schema

s3_client = boto3.client('s3')

@tracer.capture_method
def store_conversation(body):
    user_id = body.get('userID')
    topic_id = body.get('topicID')
    conversation_text = body.get('text')
    createdDate = body.get('createdDate')


    # Get User and Topic objects from the database
    with session:
        user = session.query(User).filter_by(id=user_id).first()
        topic = session.query(Topic).filter_by(id=topic_id).first()

        # If user or topic doesn't exist, return an error message (optional)
        if user is None and topic is None:
            return {"statusCode": 400, "body": f"User with ID {user_id} not found. Topic with ID {topic_id} not found."}
        elif user is None:
            return {"statusCode": 400, "body": f"User with ID {user_id} not found."}
        elif topic is None:
            return {"statusCode": 400, "body": f"Topic with ID {topic_id} not found."}


    s3_key = generate_s3_key("conversations", createdDate, user_id)
    
    s3_client.put_object(Body=conversation_text, Bucket=s3_bucket, Key=s3_key)
    
    
    with session:
        # Create a new Conversation object
        conversation = Conversation(
                            s3_bucket=s3_bucket,
                            s3_key=s3_key,
                            title=body.get('title'),
                            isPublic=body.get('isPublic'),
                            createdDate=body.get('createdDate'),
                            userID=user.id,
                            topicID=topic.id
                        )
    
        session.add(conversation)
        session.commit()

# @validate(inbound_schema=conversation_schema)
@app.post("/store_conversation")
def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    response = store_conversation(body)
    
    if 'statusCode' in response and response['statusCode'] != 200:
        return response
        
    return {"statusCode": 200, "body": "Data stored successfully!"}