#! /usr/bin/python3
import re
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/l2go', methods=['POST'])
def decode_l2go_path():
    data = request.get_json()
    video_url = data['video_url']
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


if __name__ == "__main__":
    app.run()