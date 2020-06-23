<!-- PROJECT LOGO -->
<br />
<p align="center">
  <img src="https://github.com/TheNerdful8/Lecture2Gether/blob/master/lecture2gether-vue/src/assets/Lecture2Gether_stroke.svg" alt="Logo" width="240" height="240">
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

![Flask CI](https://github.com/TheNerdful8/Lecture2Gether/workflows/Flask%20CI/badge.svg?branch=master) &nbsp;&nbsp; ![Node.js CI](https://github.com/TheNerdful8/Lecture2Gether/workflows/Node.js%20CI/badge.svg)

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
* [Prometheus Flask exporter](https://github.com/rycus86/prometheus_flask_exporter)
* [Prometheus Python Client](https://github.com/prometheus/client_python)
* [gevent](http://gevent.org)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [Google API Python Client](https://github.com/googleapis/google-api-python-client/)
* [Nose](https://nose.readthedocs.io/en/latest/)
* [Redis](https://redis.io/)
* [coolname](https://github.com/alexanderlukanin13/coolname)


<!-- TODO: Installation for frontend -->
## Install
### Using docker (or podman)
You can either build the image from source or use one of the provided versions from our
[Docker Hub Repository](https://hub.docker.com/r/thenerdful8/lecture2gether).

```bash
# for building from source
docker build -t lecture2gether
docker run -p 8000:8000 lecture2gether

# for running from docker hub
docker run -p 8000:8000 thenerdful8/lecture2gether
```

This will start the whole application stack and expose it at
[http://localhost:8000/](http://localhost:8000).

### Install single Backend
The backend runs on a redis database.
Run the redis docker `docker run -it -p 6379:6379 redis:buster` or install manually by following [this guide](https://redis.io/topics/quickstart#installing-redis-more-properly).
Set the environment-variables `'REDIS_HOST', 'REDIS_PORT', 'REDIS_DB', 'REDIS_PASSWORD'`
accordingly.
```bash
#Clone the repository
git clone https://github.com/TheNerdful8/Lecture2Gether

#Go to the backend folder
cd Lecture2Gether/lecture2gether_flask/

#Get Poetry
pip3 install poetry --user

#install the dependencies
poetry install --no-root

#start the server manually
poetry run python app.py
```

### Install single Frontend
Install [npm](https://nodejs.org/en/download) on your machine
```bash
#Clone the repository
git clone https://github.com/TheNerdful8/Lecture2Gether

#Go to the frontend folder
cd Lecture2Gether/lecture2gether-vue/

#Install required npm dependencies
npm install

#Run the application with
npm run serve
```

## Configuration
There are two main ways of configuring the application.
While the defaults were chosen in such a way that they work in a development environment
(the docker container has different [ones](./docker/settings.json)) they might need change in a production setup.

The server can be configured via the following environment variables
Name | Default Value | Description
-----|---------------|------------
SECRET\_KEY | codenames | **Change this in production**
REDIS\_HOST | localhost | Hostname of the redis database which should be used
REDIS\_PORT | 6379 | Port on which redis listens on the redis-host
REDIS\_DB | 0 | Which database on the  redis server should be used
REDIS\_PASSWORD | *empty* | Password to authenticate at the redis server
CLEANUP\_INTERVAL | 900 | Interval (in seconds) of searching for abandoned rooms
CLEANUP\_ROOM\_EXPIRE\_TIME | 3600 | Time (in seconds) until an empty room gets abandoned
CLEANUP_ROOM_LIFE_TIME | 86400 | Time (in seconds) until an active room gets abandoned
LOGLEVEL | INFO | Configures the python logging loglevel
GOOGLE\_API\_KEY | *empty* | A Google API key, used to extract meta data from YouTube videos

The frontend is configured via a `settings.json` file which should be reachable on a
request to `/` from the running browser application.
The format is as follows:
```
{
    "apiRoot": <string>,        // Under which url the server is reachable for http api calls
    "socketioHost": <string>,   // Under which host the socket.io endpoint is served.
                                // Can be empty which results in the same as one as where the frontend is deployed
    "environment": <string>     // Not yet used but necessary
}
```

## Statistics
The backend publishes statistical data (No. sessions, No. joined/left rooms, server infos, ...) in the [Prometheus](https://prometheus.io/) format to `/metrics`. This can be scraped by a [Prometheus](https://prometheus.io/) server and displayed in e.g. [Grafana](https://grafana.com/).

## License

Distributed under the MIT License. See `LICENSE` for more information.
