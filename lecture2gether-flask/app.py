"""Flask server for Codenames"""
# pylint: disable=C0103

import logging
import json
import os
from secrets import token_urlsafe
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room, close_room, send, emit, rooms
from datetime import datetime, timedelt 

ACTIVE_CLIENTS = 0
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "codenames")

ROOM_STATES = {}
ROOM_USER_COUNT = {}

@socketio.on('connect')
def on_connect():
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS += 1

@socketio.on('disconnect')
def on_disconnect():
    global ACTIVE_CLIENTS
    global ROOM_USER_COUNT
    global ROOM_STATES
    ACTIVE_CLIENTS -= 1
    for room in rooms(sid=request.sid):
        if room in ROOM_USER_COUNT.keys():
            ROOM_USER_COUNT[room] -= 1
            if ROOM_USER_COUNT[room] <= 0:
                del ROOM_USER_COUNT[room]
                del ROOM_STATES[room]

@socketio.on('create')
def on_create(init_state):
    """Create a watch room"""
    room_token = token_urlsafe(24)

    state = add_current_time_to_state(init_state)
    state = add_set_time_to_state(state)

    global ROOM_STATES
    ROOM_STATES[room_token] = state
    ROOM_USER_COUNT[room_token] = 1

    join_room(room_token)

    emit('join_room', {'roomId': room_token}, room=room_token)
    emit('video_state_update', state, room=room_token)


@socketio.on('join')
def on_join(data):
    """Join a watch room"""
    room_token = data['roomId']

    global ROOM_STATES
    global ROOM_USER_COUNT
    state = add_current_time_to_state(ROOM_STATES[room_token])
    ROOM_USER_COUNT[room_token] += 1

    join_room(room_token)
    emit('video_state_update', state, room=room_token)

@socketio.on('leave')
def on_leave(data):
    """Leave a watch room"""
    room = data['roomId']

    global ROOM_USER_COUNT
    global ROOM_STATES

    ROOM_USER_COUNT[room] -= 1

    if ROOM_USER_COUNT[room] <= 0:
        del ROOM_USER_COUNT[room]
        del ROOM_STATES[room]
        
    leave_room(room)

@socketio.on('video_state_set')
def on_video_state_set(state):
    """Join a watch room"""
    room_token = state['roomId']

    state = add_current_time_to_state(state)
    state = add_set_time_to_state(state)

    global ROOM_STATES
    ROOM_STATES[room_token] = state

    join_room(room_token)

    emit('video_state_update', state, room=room_token)

def add_current_time_to_state(state):
    state['currentTime'] = datetime.now().timestamp()
    return state

def add_set_time_to_state(state):
    state['setTime'] = datetime.now().timestamp()
    return state

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False
    app.config['DEBUG'] = os.environ.get('DEBUG', False)

    socketio.run(app, host='0.0.0.0')
