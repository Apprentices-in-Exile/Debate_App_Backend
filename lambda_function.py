import requests
import json 
import pymysql 
from requests import Response
from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.orm import Session
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from database_credentials import get_db_url
from globals import tracer, logger, metrics
from globals import engine

@metrics.log_metrics
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    global engine

    # Parse path and body from the event
    path = event.get('path')
    body = json.loads(event.get('body', '{}'))

    # Initialize SQLAlchemy engine if it's not already initialized
    if engine is None:
        db_url = get_db_url()
        engine = create_engine(db_url)


    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Success!'
        })
    }