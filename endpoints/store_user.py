import json 
from aws_lambda_powertools.utilities.validation import validate

from models.users import User

from globals import tracer
from globals import app
from session import session
# from schemas.conversation import conversation as conversation_schema


@tracer.capture_method
def store_user(body):

    user = User(
                userName=body.get('userName'),
                firstName=body.get('firstName'),
                lastName=body.get('lastName'),
                email=body.get('email'),
                createdDate=body.get('createdDate')
            )
            

    # Store the Conversation object in the database
    with session:
        session.add(user)
        session.commit()

# @validate(inbound_schema=conversation_schema)
@app.post("/store_user")
def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    store_user(body)
    return {"statusCode": 200, "body": "Data stored successfully!"}