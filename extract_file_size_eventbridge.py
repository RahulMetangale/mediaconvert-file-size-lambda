import json
import boto3
import urllib.parse

s3 = boto3.client("s3")
eventbridge = boto3.client("events")
EVENT_BUS_NAME="Your_Service_Bus_Name"

def lambda_handler(event, context):
    print("Event:", json.dumps(event, indent=2))
    
    # Extract MediaConvert output details
    job_detail = event["detail"]
    output_files = job_detail["outputGroupDetails"][0]["outputDetails"]

    file_events = []
    for output in output_files:
        output_s3_uri = output["outputFilePaths"][0]
        
        # Extract S3 bucket and key
        parsed_url = urllib.parse.urlparse(output_s3_uri)
        s3_bucket = parsed_url.netloc
        s3_key = parsed_url.path.lstrip('/')

        # Get file size from S3
        response = s3.head_object(Bucket=s3_bucket, Key=s3_key)
        file_size_bytes = response["ContentLength"]
        file_size_gb = file_size_bytes / (1024 ** 3)
        
        # Create an EventBridge event structure
        file_event = {
            "Source": "custom.mediaconvert",
            "DetailType": "MediaConvertJobCompleted",
            "Detail": json.dumps({
                "file_path": output_s3_uri,
                "file_size_gb": round(file_size_gb, 2),
                "job_id": job_detail["jobId"]
            }),
            "EventBusName": EVENT_BUS_NAME
        }
        file_events.append(file_event)
      
    eventbridge.put_events(Entries=file_events)
    return {"statusCode": 200, "body": json.dumps("Notification Sent")}
