import boto3
from botocore.exceptions import ClientError

class DdbHelpers():

    def __init__(self, table_name):
        self.dynamodb_client = boto3.client('dynamodb')
        self.table_name = table_name
        pass

    def get_brags(self, table_name):
        try:
            scan_response = self.dynamodb_client.scan(
                TableName=table_name,
                )
            scan_response = [{"body": brag["body"]["S"], "title": brag["title"]["S"],
                "id": brag["id"]["S"], "creation_time": brag["creation_time"]["N"]} for brag in scan_response['Items']]
        except ClientError as e:
            scan_response = e.response['Error']['Code']
            raise
        return scan_response

    def create_brag(self, table_name, data):
        try:
            put_response = self.dynamodb_client.put_item(
                TableName=table_name,
                Item={
                    "title": {
                        "S": data['title']
                    },
                    "body": {
                        "S": data['body']
                    },
                    "id": {
                        "S": data['id']
                    },
                    "creation_time": {
                        "N": data['creation_time']
                    }
                },
                ConditionExpression='attribute_not_exists(id)'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                put_response = (" ").join(['Item with id', data['id'], 'already exists!'])
            else:
                put_response = e.response['Error']['Code']
                raise
        return put_response

    def update_brag(self, table_name, data):
        try:
            update_response = self.dynamodb_client.update_item(
                TableName='brag-posts',
                Key={
                    'id': {
                        "S": data['id']
                    }
                },
                UpdateExpression="set title = :t, body=:b",
                ExpressionAttributeValues={
                    ':t': {
                        "S": data['title']
                        },
                    ':b': {
                        "S": data['body']
                    },
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            update_response = e.response['Error']['Code']
            raise
        return update_response
