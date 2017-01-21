import sys
import logging
import urlparse
import json

from chalice import Chalice

app = Chalice(app_name='brag')
app.log.setLevel(logging.DEBUG)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    # get posts from db here
    posts = [
        {"title": "hey i did a thing", "body": "i did it like this", "id": 0},
        {"title": "i did another thing", "body": "i did it like this", "id": 1},
        {"title": "check out the latest thing i did", "body": "i did it like this", "id": 2},
        ]
    return { 'posts': posts }

@app.route('/new', methods=['POST'], content_types=['application/json'])
def post():
    data = app.current_request.json_body
    data = json.loads(data['post'])
    title = data['title']
    body = data['body']
    return {
        'title': title,
        'body': body,
    }

@app.route('/comment', methods=['POST'], content_types=['application/json'])
def comment():
    data = app.current_request.json_body
    data = json.loads(data['post'])
    post = data['post']
    comment = data['comment']
    return {
        'post': post,
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
