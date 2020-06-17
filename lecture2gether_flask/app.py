#!/usr/bin/env python3
from gevent import monkey
monkey.patch_all()

import os
import json
import time
import logging
from datetime import datetime
from time import sleep
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
from redis.client import Redis
from redis.exceptions import ConnectionError
from threading import Thread
from urllib.parse import urlparse
from coolname import generate_slug
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge, Counter

from meta_data_provider import L2GoMetaDataProvider, VideoNotFoundException, VideoUnauthorizedException, \
    YouTubeMetaDataProvider, DefaultMetaDataProvider

logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO'))

# Crete app
app = Flask(__name__)
app.config['DEBUG'] = True

# Create prometheus metrics for e.g. grafana
os.environ["DEBUG_METRICS"] = "false" # This needs to be false (see doc)
metrics = PrometheusMetrics(app=app, path='/metrics')

# Create non decorator defined metrics
active_clients_metric = Gauge('l2g_clients_active', 'Number of active clients')
room_clean_metric = Counter('l2g_room_cleaned', 'Number of rooms cleaned by the room cleaner')

# Enable cross origin resource sharing in debug mode
if app.config['DEBUG']:
    CORS(app)

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

# Kick dead sessions (cause socket.io reloaded) out of rooms
for room_token, room in db.hgetall('rooms').items():  # For all rooms in db
    room = json.loads(room) # Deserialize room data
    room['count'] = 0 # Set connections to 0 because no body can be connected
    db.hset('rooms', room_token, json.dumps(room))
    logging.info("Kick dead sessions out of room {}".format(room_token))

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
                room_clean_metric.inc()
        logging.info("Waiting for room cleanup")
        time.sleep(cleanup_interval)

#Create deamon itself
cleanup_thread = Thread(target=room_cleanup, daemon=True)
cleanup_thread.start()

@app.route('/api/metadata', methods=['POST'])
@metrics.counter('l2g_video_url_parsed', 'Number of Lecture2Go videos parsed')
def decode_l2go_path():
    """Decodes a lecture2go video url"""
    data = request.get_json()

    if not data or not 'video_url' in data:
        abort(400)

    video_url = data['video_url']

    password = ''
    if 'password' in data:
        password = data['password']

    url = urlparse(video_url)

    try:
        if url.hostname in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            meta_data_provider = YouTubeMetaDataProvider(video_url)
        elif 'lecture2go' in url.hostname or '/l2go/' in url.path:
            meta_data_provider = L2GoMetaDataProvider(video_url, password)
        else:
            meta_data_provider = DefaultMetaDataProvider(video_url)
    except VideoNotFoundException:
        abort(404)
    except VideoUnauthorizedException:
        abort(401)

    video_meta_data = meta_data_provider.get_meta_data()

    return jsonify(video_meta_data)

@socketio.on('connect')
@metrics.counter('l2g_sockets_connected', 'Number of connections ever made')
def on_connect():
    """Handles websocket creation event"""
    active_clients_metric.inc()

@socketio.on('disconnect')
def on_disconnect():
    """Handles websocket disconnection event"""
    active_clients_metric.dec()

    # Decrease room client counts
    for room_token in rooms(sid=request.sid):  # For all rooms of user
        if db.hexists('rooms', room_token):  # If room exists
            room = json.loads(db.hget('rooms', room_token))
            room['count'] -= 1
            emit('room_user_count_update', {"users": room['count']}, room=room_token)
            db.hset('rooms', room_token, json.dumps(room))

@socketio.on('create')
@metrics.counter('l2g_rooms_created', 'Increases if a room is created')
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
@metrics.counter('l2g_rooms_joined', 'Increases if a room is joined')
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
@metrics.counter('l2g_rooms_left', 'Rooms actively left by the client')
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
@metrics.counter('l2g_video_state_updates', 'Number of video state updates')
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
@metrics.counter('l2g_chat_messages_send', 'Number of broadcasted chat messages')
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
