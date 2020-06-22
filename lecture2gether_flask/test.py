#!/usr/bin/env python3
import os
from datetime import datetime

import os
import time

from app import app, socketio
from meta_data_provider import youtube_video_id_from_url, L2GoMetaDataProvider, YouTubeMetaDataProvider


def test_socketio():
    # log the user in through Flask test client
    flask_test_client = app.test_client()

    # connect to Socket.IO
    user_count = 10000
    room_count = 1000

    socketio_test_clients = [socketio.test_client(app, flask_test_client=flask_test_client) for i in range(user_count)]
    
    room_responses = ([client.emit("create", {'foo': 'bar'}, callback=True)[0] for client in socketio_test_clients[:room_count]])

    assert all([True for response in room_responses if response["status_code"] == 200]), "Check failed, invalid status code while room creation."

    rooms = [response['roomId'] for response in room_responses]

def test_metrics():
    flask_test_client = app.test_client()

    r = flask_test_client.get('/metrics')

    assert r.status_code == 200, f"Check failed, status code was {r.status_code}, but 200 was expected."


def test_video_parsing():
    flask_test_client = app.test_client()

    r = flask_test_client.post('/api/metadata', json={
        'username': 'python', 'password': 'is-great!'})

    assert r.status_code == 400, f"Check failed, status code was {r.status_code}, but 400 was expected."

    r = flask_test_client.post('/api/metadata', data={
        'username': 'python', 'password': 'is-great!'})

    assert r.status_code == 400, f"Check failed, status code was {r.status_code}, but 400 was expected."

    r = flask_test_client.post('/api/metadata', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577', 'password': ''})

    assert r.status_code == 200, f"Check failed, status code was {r.status_code}, but 200 was expected."

    if os.getenv("L2G_TEST_PASSWD") is not None:
        r = flask_test_client.post('/api/metadata', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/GJfhuZOP4Jc', 'password': str(os.getenv("L2G_TEST_PASSWD"))})
        assert r.status_code == 200, f"Check failed, status code was {r.status_code}, but 200 was expected."
    else:
        print("Skiping the lecture2go password positive test case, because no password secret exists.")

    r = flask_test_client.post('/api/metadata', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577'})

    assert r.status_code == 200, f"Check failed, status code was {r.status_code}, but 200 was expected."

    r = flask_test_client.post('/api/metadata', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/v/jqxTE9ZN8Q3byd2nXGMkIAxx'
    })

    assert r.status_code == 401

    r = flask_test_client.post('/api/metadata', json={
        'video_url': 'https://lecture2go.uni-hamburg.de/l2go/-/get/v/invalid'
    })

    assert r.status_code == 404


def test_l2go_metadata():
    meta_data_provider = L2GoMetaDataProvider('https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577')
    meta_data = meta_data_provider.get_meta_data()
    assert meta_data['url'] == 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577'
    assert meta_data['streamUrl'] == 'https://fms.rrz.uni-hamburg.de/vod/_definst/mp4:4l2gkoowiso/00.000_Prof.Dr.OlafAsbach_2016-03-24_14-37.mp4/playlist.m3u8'
    assert meta_data['title'] == 'Dies Academicus'
    assert meta_data['creator'] == 'Prof. Dr. Olaf Asbach'
    assert meta_data['creatorLink'] == 'https://lecture2go.uni-hamburg.de/l2go/-/get/0/0/0/0/0/?_lgopenaccessvideos_WAR_lecture2goportlet_searchQuery=Prof. Dr. Olaf Asbach'
    assert meta_data['date'] == datetime(year=2016, month=3, day=24)
    assert meta_data['license'] == 'UHH-L2G'
    assert meta_data['licenseLink'] == 'https://lecture2go.uni-hamburg.de/license-l2go'


def test_youtube_metadata():
    if 'GOOGLE_API_KEY' not in os.environ:
        return

    meta_data_provider = YouTubeMetaDataProvider('https://youtu.be/qxyQCD3QT6Y')
    meta_data = meta_data_provider.get_meta_data()
    assert meta_data['url'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y'
    assert meta_data['streamUrl'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y'
    assert meta_data['title'] == 'Cravendale Last Marble Standing E2 Balancing - Marble Race by Jelle\'s Marble Runs'
    assert meta_data['creator'] == 'Jelle\'s Marble Runs'
    assert meta_data['creatorLink'] == 'https://www.youtube.com/channel/UCYJdpnjuSWVOLgGT9fIzL0g'
    assert meta_data['date'] == datetime(year=2020, month=6, day=5, hour=17, minute=0, second=13)
    assert meta_data['license'] == 'youtube'
    assert meta_data['licenseLink'] is None


def test_youtube_metadata_no_api_key():
    API_KEY = os.environ['GOOGLE_API_KEY']
    del os.environ['GOOGLE_API_KEY']
    meta_data_provider = YouTubeMetaDataProvider('https://youtu.be/qxyQCD3QT6Y')
    meta_data = meta_data_provider.get_meta_data()
    print(meta_data)
    assert meta_data['url'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y'
    assert meta_data['streamUrl'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y'
    assert meta_data['title'] is None
    assert meta_data['creator'] is None
    assert meta_data['creatorLink'] is None
    assert meta_data['date'] is None
    assert meta_data['license'] is None
    assert meta_data['licenseLink'] is None
    os.environ['GOOGLE_API_KEY'] = API_KEY


def test_youtube_video_id_from_url():
    error_message = 'Wrong video id for url %s: %s'
    id = 'qxyQCD3QT6Y'
    url = f'https://youtu.be/{id}'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://www.youtube.com/watch?v={id}'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://www.youtube.com/watch/?v={id}'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://www.youtube.com/watch/{id}'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'http://youtube.com/watch?v={id}&gl=DE'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://youtu.be/{id}?t=9'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    listid = 'PLSmWeUDtr9fAusnPxzrAG2v1B8sMeFlbT'
    url = f'https://www.youtube.com/watch?v={id}&list={listid}&index=2'
    res = youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = 'https://www.youtube.com/channel/UCYJdpnjuSWVOLgGT9fIzL0g'
    res = youtube_video_id_from_url(url)
    assert res is None, error_message % (url, res)
    url = 'https://www.youtube.com/watch'
    res = youtube_video_id_from_url(url)
    assert res is None, error_message % (url, res)
