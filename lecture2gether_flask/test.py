#!/usr/bin/env python3
import os
import re
import time
from datetime import datetime

from app import app, socketio
from meta_data_provider import L2GoMetaDataProvider, YouTubeMetaDataProvider, GoogleDriveMetaDataProvider


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
    assert meta_data['url'] == 'https://lecture2go.uni-hamburg.de/l2go/-/get/l/4577', f" The actual url was {meta_data['url']}"
    assert re.fullmatch(r"https://fms\d*\.rrz\.uni-hamburg\.de/vod/_definst/mp4:4l2gkoowiso/00\.000_Prof\.Dr\.OlafAsbach_2016-03-24_14-37\.mp4/playlist\.m3u8", meta_data['streamUrl']) is not None, f"The actual stream url was {meta_data['streamUrl']}"
    assert meta_data['title'] == 'Dies Academicus', f" The actual title was {meta_data['title']}"
    assert meta_data['creator'] == 'Prof. Dr. Olaf Asbach', f" The creator url was {meta_data['creator']}"
    assert meta_data['creatorLink'] == 'https://lecture2go.uni-hamburg.de/l2go/-/get/0/0/0/0/0/?_lgopenaccessvideos_WAR_lecture2goportlet_searchQuery=Prof. Dr. Olaf Asbach', f" The actual creatorLink was {meta_data['creatorLink']}"
    assert meta_data['date'] == datetime(year=2016, month=3, day=24), f" The date was {meta_data['date']}"
    assert meta_data['license'] == 'UHH-L2G', f" The license was {meta_data['license']}"
    assert meta_data['licenseLink'] == 'https://lecture2go.uni-hamburg.de/license-l2go', f" The licenseLink was {meta_data['licenseLink']}"


def test_google_drive_metadata():
    if 'GOOGLE_DRIVE_API_KEY_BACKEND' not in os.environ or \
        'GOOGLE_DRIVE_API_KEY_FRONTEND' not in os.environ:
        return
    url = "https://drive.google.com/file/d/1WESi5lqI-o8N4-_gJJE4R-X87C6EyejB/view?usp=sharing"
    meta_data_provider = GoogleDriveMetaDataProvider(url)
    meta_data = meta_data_provider.get_meta_data()
    assert meta_data['url'] == url, f" The actual url was {meta_data['url']}"
    assert meta_data['streamUrl'] == f'https://www.googleapis.com/drive/v3/files/1WESi5lqI-o8N4-_gJJE4R-X87C6EyejB?key={str(os.environ["GOOGLE_DRIVE_API_KEY_FRONTEND"])}&alt=media&l2g_media_type=video/webm',  f" The actual stream url was {meta_data['streamUrl']}"
    assert meta_data['title'] == 'CI_VIDEO_DO_NOT_TOUCH.webm', f" The actual title was {meta_data['title']}"
    assert meta_data['mimeType'] == 'video/webm', f" The actual mimeType was {meta_data['mimeType']}"


def test_youtube_metadata():
    if 'GOOGLE_YOUTUBE_API_KEY' not in os.environ:
        return

    meta_data_provider = YouTubeMetaDataProvider('https://youtu.be/qxyQCD3QT6Y')
    meta_data = meta_data_provider.get_meta_data()
    assert meta_data['url'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y', f" The actual url was {meta_data['url']}"
    assert meta_data['streamUrl'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y', f" The actual streamUrl was {meta_data['streamUrl']}"
    assert meta_data['title'] == 'Cravendale Last Marble Standing E2 Balancing - Marble Race by Jelle\'s Marble Runs', f" The actual title was {meta_data['title']}"
    assert meta_data['creator'] == 'Jelle\'s Marble Runs', f" The actual creator was {meta_data['creator']}"
    assert meta_data['creatorLink'] == 'https://www.youtube.com/channel/UCYJdpnjuSWVOLgGT9fIzL0g', f" The actual creatorLink was {meta_data['creatorLink']}"
    assert meta_data['date'] == datetime(year=2020, month=6, day=5, hour=17, minute=0, second=13), f" The actual date was {meta_data['date']}"
    assert meta_data['license'] == 'youtube', f" The actual license was {meta_data['license']}"
    assert meta_data['licenseLink'] is None


def test_youtube_metadata_no_api_key():
    API_KEY = os.getenv('GOOGLE_YOUTUBE_API_KEY', "")
    if API_KEY:
        del os.environ['GOOGLE_YOUTUBE_API_KEY']
    meta_data_provider = YouTubeMetaDataProvider('https://youtu.be/qxyQCD3QT6Y')
    meta_data = meta_data_provider.get_meta_data()
    print(meta_data)
    assert meta_data['url'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y', f" The actual url was {meta_data['url']}"
    assert meta_data['streamUrl'] == 'https://www.youtube.com/watch?v=qxyQCD3QT6Y', f" The actual streamUrl was {meta_data['streamUrl']}"
    assert meta_data['title'] is None
    assert meta_data['creator'] is None
    assert meta_data['creatorLink'] is None
    assert meta_data['date'] is None
    assert meta_data['license'] is None
    assert meta_data['licenseLink'] is None
    os.environ['GOOGLE_YOUTUBE_API_KEY'] = API_KEY


def test_youtube_video_id_from_url():
    error_message = 'Wrong video id for url %s: %s'
    id = 'qxyQCD3QT6Y'
    url = f'https://youtu.be/{id}'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://www.youtube.com/watch?v={id}'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://www.youtube.com/watch/?v={id}'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://www.youtube.com/watch/{id}'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'http://youtube.com/watch?v={id}&gl=DE'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = f'https://youtu.be/{id}?t=9'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    listid = 'PLSmWeUDtr9fAusnPxzrAG2v1B8sMeFlbT'
    url = f'https://www.youtube.com/watch?v={id}&list={listid}&index=2'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res == id, error_message % (url, res)
    url = 'https://www.youtube.com/channel/UCYJdpnjuSWVOLgGT9fIzL0g'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res is None, error_message % (url, res)
    url = 'https://www.youtube.com/watch'
    res = YouTubeMetaDataProvider.youtube_video_id_from_url(url)
    assert res is None, error_message % (url, res)
