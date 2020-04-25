#!/usr/bin/env python3
import os
import re
import json
import requests
import logging
import eventlet
from datetime import datetime 
from secrets import token_urlsafe
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, close_room, emit, rooms
from redis.client import Redis


logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))
# TODO: readme redis

app = Flask(__name__)
app.config['DEBUG'] = True

if app.config['DEBUG']:
    CORS(app)

ACTIVE_CLIENTS = 0

socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "codenames")

# INIT REDIS DATEBASE
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
redis_password = os.getenv('REDIS_PASSWORD', None)
db = Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

if db.ping():
    logging.info("SUCCESS: Connected to Redis database.")
else:
    logging.error("ERROR: Connection to Redis database failed!")

@app.route('/l2go', methods=['POST'])
def decode_l2go_path():
    data = request.get_json()

    if not data or not 'video_url' in data:
        abort(400)

    video_url = data['video_url']

    password = ''
    if 'password' in data:
        password = data['password']

    try:
        r = requests.post(video_url, data={'_lgopenaccessvideos_WAR_lecture2goportlet_password': password}, headers={'User-Agent': 'Lecture2Gether'})
    except requests.exceptions.RequestException as e:
        abort(404)

    m = re.search('https://[^"]*m3u8', r.content.decode())

    if m is None:
        abort(404)

    return jsonify(m.group())

@socketio.on('connect')
def on_connect():
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS += 1

@socketio.on('disconnect')
def on_disconnect():
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS -= 1

    for room_token in rooms(sid=request.sid):  # For all rooms of user
        if db.hexists('rooms', room_token):  # If room exists
            room = json.loads(db.hget('rooms', room_token))
            room['count'] -= 1
            db.hset('rooms', room_token, json.dumps(room))

            if room['count'] <= 0:  # Delete empty rooms
                db.hdel('rooms', room_token)

@socketio.on('create')
def on_create(init_state):
    """Create a watch room"""
    while True:
        room_token = token_urlsafe(24)
        if not db.hexists('rooms', room_token):
            break

    state = add_current_time_to_state(init_state)
    state = add_set_time_to_state(state)

    room = {'state': state, 'count': 1}
    db.hset('rooms', room_token, json.dumps(room))

    join_room(room_token)

    emit({'roomId': room_token, 'status_code': 200}, room=request.sid)
    emit('video_state_update', state, room=room_token)

@socketio.on('join')
def on_join(data):
    """Join a watch room"""

    if 'roomId' not in data:
        emit({'status_code': 400}, room=request.sid)
        return

    room_token = data['roomId']

    if not db.hexists('rooms', room_token):  # Room does not exist
        emit({'status_code': 404}, room=request.sid)
        return

    room = json.loads(db.hget('rooms', room_token))

    if room_token not in rooms(sid=request.sid):  # If user NOT allready in room
        room['state'] = add_current_time_to_state(room['state'])
        room['count'] += 1
        db.hset('rooms', room_token, json.dumps(room))

        join_room(room_token)

    # Emit response anyway
    emit({'roomId': room_token,'status_code': 200}, room=request.sid)
    emit('video_state_update', room['state'], room=request.sid)

@socketio.on('leave')
def on_leave(data):
    """Leave a watch room"""
    if 'roomId' not in data:
        emit({'status_code': 400}, room=request.sid)
        return

    room_token = data['roomId']

    if not db.hexists('rooms', room_token):  # Room does not exist
        emit({'status_code': 404}, room=request.sid)
        return

    if not room_token in rooms(sid=request.sid):  # User not in room
        emit({'status_code': 403}, room=request.sid)
        return

    room = json.loads(db.hget('rooms', room_token))
    room['count'] -= 1
    db.hset('rooms', room_token, json.dumps(room))

    if room['count'] <= 0:  # Delete empty rooms
        db.hdel('rooms', room_token)

    leave_room(room_token)
    emit({'status_code': 200}, room=request.sid)

@socketio.on('video_state_set')
def on_video_state_set(state):
    # TODO: Only update params, not delete old params
    """Update a watch room"""
    if 'roomId' not in state:
        emit({'status_code': 400}, room=request.sid)
        return

    room_token = state['roomId']


    if not db.hexists('rooms', room_token):  # Room does not exist
        emit({'status_code': 404}, room=request.sid)
        return

    if not room_token in rooms(sid=request.sid):  # User not in room
        emit({'status_code': 403}, room=request.sid)
        return

    state = add_current_time_to_state(state)
    state = add_set_time_to_state(state)

    room = json.loads(db.hget('rooms', room_token))
    room['state'] = state
    db.hset('rooms', room_token, json.dumps(room))

    emit('video_state_update', state, room=room_token)
    emit({'status_code': 200}, room=request.sid)

def add_current_time_to_state(state):
    state['currentTime'] = datetime.now().timestamp()
    return state

def add_set_time_to_state(state):
    state['setTime'] = datetime.now().timestamp()
    return state


if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False

    socketio.run(app, host='0.0.0.0')
