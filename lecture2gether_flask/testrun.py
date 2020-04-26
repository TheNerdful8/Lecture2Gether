#!/usr/bin/env python3

import time
from app import app, socketio


def socketio_test():
    # log the user in through Flask test client
    flask_test_client = app.test_client()

    # Hopefully fix weird ci behaviour

    # TEST HTTP STUFF

    r = flask_test_client.post('/api/l2go', json={
        'username': 'python', 'password': 'is-great!'})
    
    assert r.status_code == 400, f"Check failed, status code was {r.status_code}, but 400 was expected."

    r = flask_test_client.post('/api/l2go', data={
        'username': 'python', 'password': 'is-great!'})
    
    assert r.status_code == 400, f"Check failed, status code was {r.status_code}, but 400 was expected."

    r = flask_test_client.post('/api/l2go', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577', 'password': ''})

    assert r.status_code == 200, f"Check failed, status code was {r.status_code}, but 200 was expected."
    
    r = flask_test_client.post('/api/l2go', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577'})

    assert r.status_code == 200, f"Check failed, status code was {r.status_code}, but 200 was expected."

    # TEST WEBSOCKET STUFF
    # connect to Socket.IO
    user_count = 10000
    room_count = 1000

    socketio_test_clients = [socketio.test_client(app, flask_test_client=flask_test_client) for i in range(user_count)]
    
    room_responses = ([client.emit("create", {'foo': 'bar'}, callback=True)[0] for client in socketio_test_clients[:room_count]])

    assert all([True for response in room_responses if response["status_code"] == 200]), "Check failed, invalid status code while room creation."

    rooms = [response['roomId'] for response in room_responses]

if __name__ == '__main__':
    socketio_test()