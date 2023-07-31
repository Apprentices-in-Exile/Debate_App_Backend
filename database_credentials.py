from globals import tracer
from aws_lambda_powertools.utilities.parameters import ParameterResolver, SSMProvider


param_resolver = ParameterResolver()

@tracer.capture_method
def get_encrypted_parameter(name):
    return param_resolver.get(name, SSMProvider)

def get_db_url():
    # Get database credentials from environment variables
    DB_HOST: str = get_encrypted_parameter("debate_app_database_host")
    DB_USERNAME: str = get_encrypted_parameter("debate_app_database_username")
    DB_PASSWORD: str = get_encrypted_parameter("debate_app_database_password")
    DB_NAME: str = get_encrypted_parameter("debate_app_database_name")
    return f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
