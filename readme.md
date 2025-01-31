## Step 1: Create SNS Topic
This will be used to send email notification

## Step 2: Create EventBridge Rule
To invoke lambda function when transcoding job completes

## Step 3: Create Lambda function
Lambda function will extract the file size information and send message to SNS topic.
### Runtime environment
Python 3.9
### Permissions:
Aamazon S3 Read Only access
SNS Publish 
