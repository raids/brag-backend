import boto3

dynamodb_client = boto3.client('dynamodb')

try:
    clean_response = dynamodb_client.batch_write_item(
        RequestItems= {
        table_name: [
        'DeleteRequest'
        ]
        },
        )

except ClientError as e:
    scan_response = e.response['Error']['Code']
    raise
return scan_response
