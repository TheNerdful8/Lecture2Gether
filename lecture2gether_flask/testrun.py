#!/usr/bin/env python3

from app import app, socketio

def socketio_test():
    # log the user in through Flask test client
    flask_test_client = app.test_client()

    # connect to Socket.IO without being logged in
    #socketio_test_client = socketio.test_client(
    #    app, flask_test_client=flask_test_client)

    # log in via HTTP
    r = flask_test_client.post('/l2go', data={
        'username': 'python', 'password': 'is-great!'})
    
    assert r.status_code == 400

    r = flask_test_client.post('/l2go', data={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/v/27934', 'password': ''})

    assert r.status_code == 200

    r = flask_test_client.post('/l2go', data={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/v/27934'})

    assert r.status_code == 200


if __name__ == '__main__':
    socketio_test()