<!-- PROJECT LOGO -->
<br />
<p align="center">
  <img src="./lecture2gether-vue/src/assets/Lecture2Gether_stroke.svg" alt="Logo" width="240" height="240">
  <h3 align="center">Lecture2Gether</h3>
  <p align="center">
    Watch online lectures together!  
    <br />
    <br />
    <a href="https://lecture2gether.eu">View Demo</a>
    ·
    <a href="https://github.com/TheNerdful8/Lecture2Gether/issues">Report Bug</a>
    ·
    <a href="https://github.com/TheNerdful8/Lecture2Gether/issues">Request Feature</a>
    ·
    <a href="https://github.com/TheNerdful8/Lecture2Gether/pulls">Send a Pull Request</a>
  </p>
</p>

## About The Project
<!-- TODO add screenshot -->

Lecture2Gether makes it possible to watch online lectures with friends by pasting a link to a [Lecture2Go](https://github.com/lecture2go/portal-6.2-ce-ga6) Video, a YouTube Video or a simple mp4 link.
The video streams are synchronized to partially restore the social aspect of campus life.

![Flask CI](https://github.com/TheNerdful8/Lecture2Gether/workflows/Flask%20CI/badge.svg?branch=master)

### Built With

* [Vue.js](https://vuejs.org)
* [Vuetify](https://vuetifyjs.com)
* [socket.io](https://socket.io)
* [video.js](https://videojs.com)
* [videojs-youtube](https://github.com/videojs/videojs-youtube)
* [videojs-contrib-hls](https://github.com/videojs/videojs-contrib-hls)
* [Flask](https://flask.palletsprojects.com)
* [Flask-SocketIO](https://flask-socketio.readthedocs.io)
* [Flask-RESTful](https://flask-restful.readthedocs.io)
* [Eventlet](http://eventlet.net)


<!-- TODO: Installation for frontend -->
## Install
### Install Backend
Clone the repository `git clone https://github.com/TheNerdful8/Lecture2Gether`.

Go to the backend folder `cd Lecture2Gether/lecture2gether_flask/`.

Get [Poetry](https://python-poetry.org/) `pip3 install poetry --user`.

The backend runs on a redis database.
Run the redis docker `docker run -it -p 6379:6379 redis:buster` or install manually by following [this guide](https://redis.io/topics/quickstart#installing-redis-more-properly).
Set the environment-variables `'REDIS_HOST', 'REDIS_PORT', 'REDIS_DB', 'REDIS_PASSWORD'`
accordingly.

Run `poetry install` to install the dependencys. 

To start the server manually type `poetry run python app.py`.

The installation will also be provided via Docker in the future.


## License

Distributed under the MIT License. See `LICENSE` for more information.
