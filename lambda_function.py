from aws_lambda_powertools.utilities.typing import LambdaContext

from session import mysql_engine
from globals import tracer, logger, metrics
from globals import engine
from endpoints.store_conversations import handler as store_handler
from endpoints.retrieve_conversation import handler as retrieve_handler


# Map route keys to handler functions
routes = {
    "POST /store": store_handler,
    "GET /retrieve/{id}": retrieve_handler
}


@metrics.log_metrics
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    global engine

    # Initialize SQLAlchemy engine if it's not already initialized
    if engine is None:
        engine = mysql_engine

    route_key = event.route_key  # API Gateway HTTP API format
    handler = routes.get(route_key)

    if handler:
        return handler(event)
    else:
        return {"statusCode": 404, "body": "Not Found"}

