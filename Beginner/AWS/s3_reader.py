import boto3
import json

def lambda_handler(event, context):
    print("Event received:", json.dumps(event, indent=2))
    bucket_name = event.get('bucket_name')
    print("Bucket name:", bucket_name)
    return {
        'statusCode': 200,
        'body': json.dumps('Message processing complete.')
    }