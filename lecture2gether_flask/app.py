#! /usr/bin/python3
import re
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/l2go')
def decode_l2go_path():
    video_id = request.args.get('video_id')
    password = request.args.get('password')

    response = get_m3u8(video_id, password=password)
    if response is None:
        response = "Invalid videoID or password does not match."

    return jsonify(response)

def get_m3u8(id, password=''):
    r = requests.post(f'https://lecture2go.uni-hamburg.de/l2go/-/get/v/{id}', data={'_lgopenaccessvideos_WAR_lecture2goportlet_password': password}, headers={'User-Agent': 'Lecture2Gether'})
    m = re.search('https://[^"]*m3u8', r.content.decode())
    if not m:
        return None
    else:
        return m.group()


if __name__ == "__main__":
    app.run()