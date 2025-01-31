import json
import boto3
import urllib.parse

s3 = boto3.client("s3")
sns = boto3.client("sns")

# REPLACE SNS ARN
SNS_TOPIC_ARN = "arn:aws:sns:your-region:your-account-id:MediaConvertNotifications"

def lambda_handler(event, context):
    print("Event:", json.dumps(event, indent=2))
    
    # Extract MediaConvert output details
    job_detail = event["detail"]
    output_files = job_detail["outputGroupDetails"][0]["outputDetails"]

    file_info = []

    for output in output_files:
        output_s3_uri = output["outputFilePaths"][0]
        
        # Extract S3 bucket and key
        parsed_url = urllib.parse.urlparse(output_s3_uri)
        s3_bucket = parsed_url.netloc
        # Extract path within the bucket
        s3_key = parsed_url.path.lstrip('/')

        # Get file size from S3
        response = s3.head_object(Bucket=s3_bucket, Key=s3_key)
        file_size_bytes = response["ContentLength"]
        file_size_gb = file_size_bytes / (1024 ** 3)

        file_info.append(f"File: {output_s3_uri}, Size: {file_size_gb : 2f} GB")

    # Send SNS notification
    message = "MediaConvert job completed.\n" + "\n".join(file_info)
    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="MediaConvert Job Completed")
    
    return {"statusCode": 200, "body": json.dumps("Notification Sent")}
