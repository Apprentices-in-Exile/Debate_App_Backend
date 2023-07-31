from aws_lambda_powertools.event_handler import ALBResolver
from aws_lambda_powertools import Logger, Metrics, Tracer

# Set up AWS Lambda Powertools
tracer = Tracer()
logger = Logger()
metrics = Metrics()

# Routing mechanism. Define routes and associate them with specific handler functions
app = ALBResolver()

engine = None