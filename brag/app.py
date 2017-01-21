import sys
import logging
import urlparse
import json
import uuid
import time
import boto3
from botocore.exceptions import ClientError

from chalice import Chalice

app = Chalice(app_name='brag')
app.log.setLevel(logging.DEBUG)
app.debug = True

dynamodb_client = boto3.client('dynamodb')
dynamodb_table = 'brag-posts'

def get_brags():
    try:
        scan_response = dynamodb_client.scan(
            TableName='brag-posts',
            )
        scan_response = [{"body": brag["body"]["S"], "title": brag["title"]["S"],
            "id": brag["id"]["S"]} for brag in scan_response['Items']]
    except ClientError as e:
        scan_response = e.response['Error']['Code']
        raise
    return scan_response

def create_brag(data):
    try:
        put_response = dynamodb_client.put_item(
            TableName=dynamodb_table,
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

def update_brag(data):
    try:
        update_response = dynamodb_client.update_item(
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

@app.route('/', methods=['GET'], cors=True)
def index():
    # get posts from db here
    # posts = [
    #     {"title": "hey i did a thing", "body": "i did it like this", "id": 0},
    #     {"title": "i did another thing", "body": "i did it like this", "id": 1},
    #     {"title": "check out the latest thing i did", "body": "i did it like this", "id": 2},
    #     ]
    brags = get_brags()
    return {
        'brags': brags,
        # 'body': body,
    }
    return { 'brags': brags }

@app.route('/brag', methods=['PUT','POST'], content_types=['application/json'], cors=True)
def brag():
    # If request is a POST, generate a uuid and create a new item in ddb
    # If request is a PUT, update the existing item in ddb
    request = app.current_request
    data = request.json_body
    data = json.loads(data['brag'])
    if request.method == 'POST':
        # generate uuid for the new post
        data['creation_time'] = str(int(time.time()))
        data['id'] = str(uuid.uuid4())
        brags = create_brag(data)
    elif request.method == 'PUT':
        brags = update_brag(data)
    return {
        'brags': brags,
    }

@app.route('/comment', methods=['POST'], content_types=['application/json'], cors=True)
def comment():
    data = app.current_request.json_body
    data = json.loads(data['comment'])
    brag = data['id']
    comment = data['comment']
    return {
        'id': id,
        'comment': comment,
    }

@app.route('/like', methods=['POST'], content_types=['application/json'], cors=True)
def comment():
    data = app.current_request.json_body
    data = json.loads(data['brag'])
    brag = data['brag']
    comment = data['comment']
    return {
        'id': id,
        'comment': comment,
    }

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.json_body
#     # Suppose we had some 'db' object that we used to
#     # read/write from our database.
#     # user_id = db.create_user(user_as_json)
#     return {'user_id': user_id}
#
# See the README documentation for more examples.
#
