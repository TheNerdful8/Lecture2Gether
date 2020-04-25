#! /usr/bin/python3
import re
import requests
import eventlet
from flask import Flask, request, jsonify, abort
import logging
import json
import os
from secrets import token_urlsafe
from flask_socketio import SocketIO, join_room, leave_room, close_room, send, emit, rooms
from datetime import datetime 

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "codenames")

ACTIVE_CLIENTS = 0
ROOM_STATES = {}
ROOM_USER_COUNT = {}

@app.route('/l2go', methods=['POST'])
def decode_l2go_path():
    data = request.get_json()

    if not data or not 'video_url' in data:
        abort(400)

    video_url = data['video_url']

    password = ''
    if 'password' in data:
        password = data['password']

    response = get_m3u8(video_url, password=password)
    if response is None:
        response = "Invalid videoURL or password does not match."

    return jsonify(response)

def get_m3u8(video_url, password=''):
    r = requests.post(video_url, data={'_lgopenaccessvideos_WAR_lecture2goportlet_password': password}, headers={'User-Agent': 'Lecture2Gether'})
    m = re.search('https://[^"]*m3u8', r.content.decode())
    if not m:
        return None
    else:
        return m.group()

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
    app.config['DEBUG'] = os.environ.get('DEBUG', True)

    socketio.run(app, host='0.0.0.0')