from aws_lambda_powertools.utilities.typing import LambdaContext

from session import mysql_engine
from globals import tracer, logger, metrics
from globals import engine
from globals import app

import endpoints.get_conversation
import endpoints.store_conversations
import endpoints.store_topic
import endpoints.store_user


@metrics.log_metrics
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    print("=-=-=-=-=-=-=lambdaaa", event)
    return app.resolve(event, context)