from aws_lambda_powertools.utilities import parameters

ssm_provider = parameters.SSMProvider()

def get_encrypted_parameter(name):
    return ssm_provider.get(name, decrypt=True)

def get_db_url():
    # Get database credentials from environment variables
    DB_HOST: str = get_encrypted_parameter("debate_app_database_host")
    DB_USERNAME: str = get_encrypted_parameter("debate_app_database_username")
    DB_PASSWORD: str = get_encrypted_parameter("debate_app_database_password")
    DB_NAME: str = get_encrypted_parameter("debate_app_database_name")
    return f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
