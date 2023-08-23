import json 
import boto3
from aws_lambda_powertools.utilities.validation import validate

# from schemas.conversation import conversation as conversation_schema

from models.conversations import Conversation
from models.topics import Topic
from models.users import User

from globals import tracer
from globals import app

from session import session
from s3_key import generate_s3_key
from s3_key import s3_bucket


s3_client = boto3.client('s3')

@tracer.capture_method
def store_conversation(body):

        
    user_id = body.get('userID')
    topic_id = body.get('topicID')
    conversation_text = body.get('text')
    createdDate = body.get('createdDate')


    with session:
        user = session.query(User).filter_by(id=user_id).first()
        topic = session.query(Topic).filter_by(id=topic_id).first()

        if user is None and topic is None:
            return {"statusCode": 400, "body": f"User with ID {user_id} not found. Topic with ID {topic_id} not found."}
        elif user is None:
            return {"statusCode": 400, "body": f"User with ID {user_id} not found."}
        elif topic is None:
            return {"statusCode": 400, "body": f"Topic with ID {topic_id} not found."}


    s3_key = generate_s3_key("conversations", createdDate, user_id)
    
    s3_client.put_object(Body=conversation_text, Bucket=s3_bucket, Key=s3_key)
    
    
    with session:
        
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

    return {"statusCode": 200, "body": "Data stored in S3 successfully!"}
    
    
# @validate(inbound_schema=conversation_schema)
@app.post("/store_conversation")
@tracer.capture_method
def handler():
    body: dict = app.current_event.json_body
    response = store_conversation(body)
    
    if 'statusCode' in response and response['statusCode'] != 200:
        return response
        
    return {"statusCode": 200, "body": "Data stored successfully!"}
