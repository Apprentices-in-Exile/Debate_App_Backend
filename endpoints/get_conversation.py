import json 
from models.conversations import Conversation 
from globals import tracer
from globals import app
from session import session

@tracer.capture_method
def get_conversation(conversation_id):

    # Get a Conversation object from the database
    with session:
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()

        if conversation is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Conversation with ID {conversation_id} not found.'})
            }
        return {"statusCode": 200, "body": json.dumps(conversation.to_dict())}
    


@app.get("/get_conversation/{id}")
def handler(event, context):
    conversation_id = int(event['pathParameters']['id'])
    response = get_conversation(conversation_id)
    return response