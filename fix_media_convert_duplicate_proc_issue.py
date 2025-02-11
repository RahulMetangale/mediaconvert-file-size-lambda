import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# DynamoDB table name for tracking processed files
# This table should already be present
DYNAMODB_TABLE = 'media_conversion_jobs'

def lambda_handler(event, context):
    # Extract bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Generate a unique identifier for the file. ID will be in the form bucket:filename
    file_id = f"{bucket}:{key}"
    
    try:
        # Check if the file has already been processed
        # Dynamo DB will be queried for this. here file_name is the key name or filed name in dynamo db table
        response = dynamodb.get_item(
            TableName=DYNAMODB_TABLE,
            Key={'file_name': {'S': file_id}}
        )
        
        if 'Item' in response:
            print(f"Duplicate file detected: {file_id}")
            return {
                'statusCode': 200,
                'body': json.dumps('Duplicate file detected')
            }
        
        # Trigger media convert job (add your Media convert processing logic here)
        print(f"Processing file: {file_id}")
        
        # Once the media convert job is triggered add a entry into dynamo table
        # Please update key name. Here file_name is the key name from dynamodb
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={'file_name': {'S': file_id}}
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('File processed successfully')
        }
    
    except ClientError as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
