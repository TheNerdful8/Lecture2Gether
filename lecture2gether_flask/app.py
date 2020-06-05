#!/usr/bin/env python3
import os
import re
import json
import time
import requests
import logging
from datetime import datetime 
from time import sleep
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, close_room, emit, rooms
from redis.client import Redis
from redis.exceptions import ConnectionError
from threading import Thread
from coolname import generate_slug

import eventlet
eventlet.monkey_patch()

logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))

# Crete app
app = Flask(__name__)
app.config['DEBUG'] = True

# Enable cross origin resource sharing in debug mode
if app.config['DEBUG']:
    CORS(app)

# Count active clients
ACTIVE_CLIENTS = 0

# Init socket.io websockets, which are used for state sync
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "codenames")

# INIT REDIS DATEBASE
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
redis_password = os.getenv('REDIS_PASSWORD', None)
db = Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)

# Wait for redis connection
while True:
    try:
        db.ping()
    except ConnectionError:
        logging.info("Waiting for connection to redis database...")
        sleep(1)
    else:
        logging.info("SUCCESS: Connected to Redis database.")
        break

# Create cleanup deamon, that deletes abandoned rooms from the database
# Get params
cleanup_interval = int(os.getenv('CLEANUP_INTERVAL', 60*15))
cleanup_room_expire_time = int(os.getenv('CLEANUP_ROOM_EXPIRE_TIME', 60*60))
# Define function that cleans abandoned rooms in an interval
def room_cleanup():
    while True:
        for room_token, room in db.hgetall('rooms').items():  # For all rooms in db
            room = json.loads(room) # Deserialize room data
            if room['count'] <= 0 and datetime.now().timestamp() - room['state']['setTime'] > cleanup_room_expire_time:  # Delete empty old rooms
                db.hdel('rooms', room_token) # Delete room
                logging.info("Delete Room {}".format(room_token))
        logging.info("Waiting for room cleanup")
        time.sleep(cleanup_interval)
        
#Create deamon itself
cleanup_thread = Thread(target=room_cleanup, daemon=True)
cleanup_thread.start()

@app.route('/api/l2go', methods=['POST'])
def decode_l2go_path():
    """Decodes a lecture2go video url"""
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
    """Handles websocket creation event"""
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS += 1

@socketio.on('disconnect')
def on_disconnect():
    """Handles websocket disconnection event"""
    global ACTIVE_CLIENTS
    ACTIVE_CLIENTS -= 1

    # Decrease room client counts
    for room_token in rooms(sid=request.sid):  # For all rooms of user
        if db.hexists('rooms', room_token):  # If room exists
            room = json.loads(db.hget('rooms', room_token))
            room['count'] -= 1
            emit('room_user_count_update', {"users": room['count']}, room=room_token)
            db.hset('rooms', room_token, json.dumps(room))

@socketio.on('create')
def on_create(init_state):
    """Create and join a watch room"""
    # Create unique token
    while True:
        room_token = generate_slug(3)
        if not db.hexists('rooms', room_token):
            break
    
    # Annotate state with timestamp
    state = add_current_time_to_state(init_state)
    state = add_set_time_to_state(state)

    # Create room in db
    room = {'state': state, 'count': 1}
    db.hset('rooms', room_token, json.dumps(room))

    # Join socket.io room
    join_room(room_token)
    
    # Publish init state
    emit('video_state_update', state, room=room_token)

    # Publish the room user count
    emit('room_user_count_update', {"users": 1}, room=room_token)
    
    # Return response
    return {'roomId': room_token, 'status_code': 200}, 200

@socketio.on('join')
def on_join(data):
    """Join a watch room"""
    # Check if all params are set
    if 'roomId' not in data:
        return {'status_code': 400}, 400
    
    room_token = data['roomId']

    # Check if room exist
    if not db.hexists('rooms', room_token):
        return {'status_code': 404}, 404

    # Get room from db
    room = json.loads(db.hget('rooms', room_token))
    
    # Add current server time to state
    room['state'] = add_current_time_to_state(room['state'])

    # Check if user is in the room
    if room_token not in rooms(sid=request.sid):
        # Increase clients in room
        room['count'] += 1
        # Save data in db
        db.hset('rooms', room_token, json.dumps(room))
        # Join the socket.io room
        join_room(room_token)
        # Notify the others about the increased user count
        message = {"users": room['count']}
        emit('room_user_count_update', message, room=room_token)

    # Emit room state
    emit('video_state_update', room['state'], room=request.sid)
    # Return response
    return {'roomId': room_token,'status_code': 200}, 200

@socketio.on('leave')
def on_leave(data):
    """Leave a watch room"""
    # Check if all params are set
    if 'roomId' not in data:
        return {'status_code': 400}, 400

    room_token = data['roomId']

    # Check if room exist
    if not db.hexists('rooms', room_token):
        return {'status_code': 404}, 404
    
    # Check if user wasnt in the room
    if not room_token in rooms(sid=request.sid):
        return {'status_code': 403}, 403

    # Get room from db
    room = json.loads(db.hget('rooms', room_token))
    # Deacrease active users in room
    room['count'] -= 1
    # Notify the others about the decreased user count
    emit('room_user_count_update', {"users": room['count']}, room=room_token)
    # Save in db
    db.hset('rooms', room_token, json.dumps(room))
    # Leave the socket.io room
    leave_room(room_token)
    # Return status
    return {'status_code': 200}, 200

@socketio.on('video_state_set')
def on_video_state_set(state):
    """Update a watch room"""
    # Check if all params are set
    if 'roomId' not in state:
        return {'status_code': 400}, 400

    room_token = state['roomId']
    
    # Check if room exist
    if not db.hexists('rooms', room_token):
        {'status_code': 404}, 404

    # Check if user wasnt in the room
    if not room_token in rooms(sid=request.sid):
        return {'status_code': 403}, 403

    # Annotate state with server timestamp
    state = add_current_time_to_state(state)
    state = add_set_time_to_state(state)

    # Get room from db
    room = json.loads(db.hget('rooms', room_token))
    # Update last state in db with new state
    room['state'] = state
    # Save db
    db.hset('rooms', room_token, json.dumps(room))
    # Publish new state to everybody in the room
    emit('video_state_update', state, room=room_token)
    # Response
    return {'status_code': 200}, 200

@socketio.on('chat_send')
def on_chat_send(message):
    """Broadcast chat message to a watch room"""
    # Check if params are correct
    if 'roomId' not in message:
        return {'status_code': 400}, request.sid

    room_token = message['roomId']

    # Check if room exist
    if not db.hexists('rooms', room_token):
        {'status_code': 404}, request.sid

    # Check if user wasnt in the room
    if not room_token in rooms(sid=request.sid):
        return {'status_code': 403}, request.sid
    
    # Add current sever timestamp to the state
    message = add_current_time_to_state(message)

    # Send message to everybody in the room
    emit('message_update', message, room=room_token)
    # Response
    return {'status_code': 200}, 200

def add_current_time_to_state(state):
    """Annotate state with the latest server time"""
    state['currentTime'] = datetime.now().timestamp()
    return state

def add_set_time_to_state(state):
    """Annotate state the time of state creation"""
    state['setTime'] = datetime.now().timestamp()
    return state

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False

    socketio.run(app, host='0.0.0.0')
