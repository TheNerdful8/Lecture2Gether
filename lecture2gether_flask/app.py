#!/usr/bin/env python3
import os
import re
import json
import time
import requests
import logging
from datetime import datetime 
from secrets import token_urlsafe
from time import sleep
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, close_room, emit, rooms
from redis.client import Redis
from redis.exceptions import ConnectionError
from threading import Thread

import eventlet
eventlet.monkey_patch()

logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))

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

while True:
    try:
        db.ping()
    except ConnectionError:
        logging.info("Waiting for connection to redis database...")
        sleep(1)
    else:
        logging.info("SUCCESS: Connected to Redis database.")
        break

# Create cleanup thread
cleanup_interval = os.getenv('CLEANUP_INTERVAL', 60*15)
cleanup_room_expire_time = os.getenv('CLEANUP_ROOM_EXPIRE_TIME', 60*60)

def room_cleanup():
    while True:
        for room_token, room in db.hgetall('rooms'):  # For all rooms in db
            room = json.loads(room)
            if room['count'] <= 0 and datetime.now().timestamp() - room['state']['setTime'] > cleanup_room_expire_time:  # Delete empty old rooms
                db.hdel('rooms', room_token)
                logging.info("Delete Room {}".format(room_token))
        logging.info("Waiting for room cleanup")
        time.sleep(cleanup_interval)

cleanup_thread = Thread(target=room_cleanup, daemon=True)
cleanup_thread.start()

@app.route('/api/l2go', methods=['POST'])
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

    title = re.search('<title>(.*)</title>', r.content.decode())
    if title.groups()[0] == 'Catalog - Lecture2Go':
        # Redirected to catalog means video does not exist
        abort(404)

    m = re.search('https://[^"]*m3u8', r.content.decode())

    if m is None:
        # No m3u8 file found means wrong (or no) password
        if password:
            abort(403)
        else:
            abort(401)

    return jsonify(m.group())

@socketio.on('connect')
def on_connect():
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS += 1

@socketio.on('disconnect')
def on_disconnect():
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS -= 1

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

    emit('video_state_update', state, room=room_token)
    return {'roomId': room_token, 'status_code': 200}, 200

@socketio.on('join')
def on_join(data):
    """Join a watch room"""

    if 'roomId' not in data:
        return {'status_code': 400}, 400

    room_token = data['roomId']

    if not db.hexists('rooms', room_token):  # Room does not exist
        return {'status_code': 404}, 404

    room = json.loads(db.hget('rooms', room_token))

    if room_token not in rooms(sid=request.sid):  # If user NOT allready in room
        room['state'] = add_current_time_to_state(room['state'])
        room['count'] += 1
        db.hset('rooms', room_token, json.dumps(room))

        join_room(room_token)

    # Emit response anyway
    emit('video_state_update', room['state'], room=request.sid)
    return {'roomId': room_token,'status_code': 200}, 200

@socketio.on('leave')
def on_leave(data):
    """Leave a watch room"""
    if 'roomId' not in data:
        return {'status_code': 400}, 400

    room_token = data['roomId']

    if not db.hexists('rooms', room_token):  # Room does not exist
        return {'status_code': 404}, 404

    if not room_token in rooms(sid=request.sid):  # User not in room
        return {'status_code': 403}, 403

    room = json.loads(db.hget('rooms', room_token))
    room['count'] -= 1
    db.hset('rooms', room_token, json.dumps(room))

    leave_room(room_token)
    return {'status_code': 200}, 200

@socketio.on('video_state_set')
def on_video_state_set(state):
    """Update a watch room"""
    if 'roomId' not in state:
        return {'status_code': 400}, 400

    room_token = state['roomId']

    if not db.hexists('rooms', room_token):  # Room does not exist
        {'status_code': 404}, 404

    if not room_token in rooms(sid=request.sid):  # User not in room
        return {'status_code': 403}, 403

    state = add_current_time_to_state(state)
    state = add_set_time_to_state(state)

    room = json.loads(db.hget('rooms', room_token))
    room['state'] = state
    db.hset('rooms', room_token, json.dumps(room))

    emit('video_state_update', state, room=room_token)
    return {'status_code': 200}, 200

@socketio.on('chat_send')
def on_chat_send(message):
    """Broadcast chat message to a watch room"""
    if 'roomId' not in message:
        return {'status_code': 400}, request.sid

    room_token = message['roomId']

    if not db.hexists('rooms', room_token):  # Room does not exist
        {'status_code': 404}, request.sid

    if not room_token in rooms(sid=request.sid):  # User not in room
        return {'status_code': 403}, request.sid

    message = add_current_time_to_state(message)

    emit('message_update', message, room=room_token)
    return {'status_code': 200}, 200

def add_current_time_to_state(state):
    state['currentTime'] = datetime.now().timestamp()
    return state

def add_set_time_to_state(state):
    state['setTime'] = datetime.now().timestamp()
    return state

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False

    socketio.run(app, host='0.0.0.0')
