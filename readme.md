## Purpose:
Get transcoded file size information after transcoding job is complete.
MediaConvert sends the event for COMPLETE when all outputs are written to Amazon S3 without errors. This event information does not contain file size. The following JSON is an example event containing the COMPLETE status for a job.
`{
    "version": "0",
    "id": "1234abcd-12ab-34cd-56ef-1234567890ab",
    "detail-type": "MediaConvert Job State Change",
    "source": "aws.mediaconvert",
    "account": "111122223333",
    "time": "2022-12-19T19:07:12Z",
    "region": "us-west-2",
    "resources": [
        "arn:aws:mediaconvert:us-west-2::jobs/1671476818694-phptj0"
    ],
    "detail": {
        "timestamp": 1671476832124,
        "accountId": "111122223333",
        "queue": "arn:aws:mediaconvert:us-west-2:111122223333:queues/Default",
        "jobId": "1671476818694-phptj0",
        "status": "COMPLETE",
        "userMetadata": {},
        "warnings": [
            {
                "code": 000000,
                "count": 1
            }
        ],
        "outputGroupDetails": [
            {
                "outputDetails": [
                    {
                        "outputFilePaths": [
                            "s3://amzn-s3-demo-bucket/file/file.mp4"
                        ],
                        "durationInMs": 30041,
                        "videoDetails": {
                            "widthInPx": 1920,
                            "heightInPx": 1080,
                            "qvbrAvgQuality": 7.38,
                            "qvbrMinQuality": 7,
                            "qvbrMaxQuality": 8,
                            "qvbrMinQualityLocation": 2168,
                            "qvbrMaxQualityLocation": 25025
                        }
                    }
                ],
                "type": "FILE_GROUP"
            }
        ],
        "paddingInserted": 0,
        "blackVideoDetected": 10,
        "blackSegments": [
            {
                "start": 0,
                "end": 10
            }
        ]
    }
}`


## Expectation
Get email notification in following format with file size information  
MediaConvert job completed.
File: <File Path>, Size:  <Size> GB

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
