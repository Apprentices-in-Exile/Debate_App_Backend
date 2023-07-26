import logging
import pymysql
import boto3
import json
from typing import Any, Dict, Union

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Union[int, str]]:
    # Initialize the logging configuration
    logging.basicConfig(level=logging.INFO)

    # Check path parameter from the event
    if 'path' not in event:
        logging.error('Missing path parameter in the event.')
        return {
            'statusCode': 400,
            'body': 'Missing path parameter in the event.'
        }
    path = event['path']

    # Check body from the event
    if 'body' not in event:
        logging.error('Missing body in the event.')
        return {
            'statusCode': 400,
            'body': 'Missing body in the event.'
        }

    # Attempt to parse the body
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        logging.error('Failed to parse body, expecting JSON.')
        return {
            'statusCode': 400,
            'body': 'Failed to parse body, expecting JSON.'
        }

    # Your actual RDS MySQL credentials and endpoint
    db_host = 'your_rds_endpoint'
    db_user = 'your_username'
    db_password = 'your_password'
    db_name = 'your_database_name'
    
    # Connect to the database
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conn.cursor()

        # Determine the operation based on the path
        if path == '/store':
            # Check necessary fields in body
            if not all(key in body for key in ('document_id', 's3_bucket', 's3_key')):
                logging.error('Missing document_id, s3_bucket, or s3_key in the body.')
                return {
                    'statusCode': 400,
                    'body': 'Missing document_id, s3_bucket, or s3_key in the body.'
                }
            
            document_id = body.get('document_id')
            s3_bucket = body.get('s3_bucket')
            s3_key = body.get('s3_key')

            try:
                query = "INSERT INTO documents (document_id, s3_bucket, s3_key) VALUES (%s, %s, %s)"
                cursor.execute(query, (document_id, s3_bucket, s3_key))
                conn.commit()
            except Exception as e:
                logging.error(f'Failed to store document in the database: {str(e)}')
                return {
                    'statusCode': 500,
                    'body': f'Failed to store document in the database: {str(e)}'
                }
            finally:
                cursor.close()
                conn.close()

            return {
                'statusCode': 200,
                'body': f'Document {document_id} saved to RDS MySQL successfully!'
            }

        elif path == '/retrieve':
            # Check necessary field in body
            if 'document_id' not in body:
                logging.error('Missing document_id in the body.')
                return {
                    'statusCode': 400,
                    'body': 'Missing document_id in the body.'
                }
            
            document_id = body.get('document_id')

            try:
                query = "SELECT s3_bucket, s3_key FROM documents WHERE document_id = %s"
                cursor.execute(query, (document_id,))
                record = cursor.fetchone()

                if record is None:
                    logging.error(f'Document with ID {document_id} not found.')
                    return {
                        'statusCode': 404,
                        'body': f'Document with ID {document_id} not found.'
                    }

                s3_bucket, s3_key = record

                s3 = boto3.client('s3')
                try:
                    response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
                    data = response['Body'].read().decode('utf-8')  # Assuming the data is text

                    return {
                        'statusCode': 200,
                        'body': 'Data retrieved successfully!',
                        'data': data
                    }
                except Exception as e:
                    logging.error(f'Error retrieving data from S3: {str(e)}')
                    return {
                        'statusCode': 500,
                        'body': f'Error retrieving data from S3: {str(e)}'
                    }
            finally:
                cursor.close()
                conn.close()

        else:
            logging.error(f'Invalid path: {path}')
            return {
                'statusCode': 400,
                'body': f'Invalid path: {path}'
            }
    except Exception as e:
        logging.error(f'Error connecting to the database: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Error connecting to the database: {str(e)}'
        }
