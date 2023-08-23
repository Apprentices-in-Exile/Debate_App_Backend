import boto3
import uuid
from datetime import datetime

s3_client = boto3.client('s3')

s3_bucket = "debate-app-data"

def generate_s3_key(folder_name, created_date, user_id):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    return f"{folder_name}/{created_date}/{user_id}/{timestamp}_{uuid.uuid4()}.json"