import json 
import boto3
import requests
from requests import Response
from models.conversations import Conversation 
from globals import tracer
from globals import app
from globals import logger
from session import session

s3_client = boto3.client('s3')

@tracer.capture_method
def get_conversation(conversation_id):


    with session:
        conversation_data = session.query(Conversation).filter_by(id=conversation_id).first()

        if conversation_data is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Conversation with ID {conversation_id} not found.'})
            }
        
        try:
            conversation_text = s3_client.get_object(
                Bucket=conversation_data.s3_bucket,
                Key=conversation_data.s3_key,
            )['Body'].read().decode('utf-8')
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': f'Error fetching data from S3: {str(e)}'})
            }
        
        conversation_dict = conversation_data.to_dict()
        conversation_dict["text"] = conversation_text
        
        return {"statusCode": 200, "body": json.dumps(conversation_dict)}



@app.get("/get_conversation/<id>")
def handler(id):
    logger.info("id is ", id)
    response = get_conversation(int(id))
    return response