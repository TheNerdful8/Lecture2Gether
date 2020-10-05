# Container build stage layout are as followed:
#      debian         node
#        |             |
#       base           |
#     /      \         |
#     |   backend  frontend
#     |         \   /
#    dev        final
#
# base: necessary base runtime and build dependencies like python
# backend: installed backend src-code
# fronted: installed frontend src-code
# dev: configuration links but no code since that gets mounted
# final: final image which is simply runnable and built by dockerhub
#

FROM debian:buster AS base

# Install normal dependencies
RUN apt-get update
RUN apt-get -y --no-install-recommends install python3 python3-pip python3-setuptools python3-openssl netbase nginx redis-server supervisor build-essential python3-dev


# Build dev-image
FROM base as dev
RUN apt-get -y --no-install-recommends install curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get -y --no-install-recommends install tmux nodejs python3-venv redis
RUN pip3 install wheel
RUN pip3 install poetry

ADD docker/dev_cmd.sh /app/src/cmd.sh
ADD docker/nginx.conf /etc/nginx/sites-enabled/default
CMD /app/src/cmd.sh


# Add project code to container
FROM base AS backend
ADD lecture2gether_flask /app/src/backend

# Setup backend
RUN pip3 install wheel
RUN pip3 install poetry
WORKDIR /app/src/backend
RUN poetry export --without-hashes -nf requirements.txt -o requirements.txt
RUN pip3 install -r requirements.txt

# Clean apt
RUN apt-get remove --autoremove -y build-essential python3-dev python3-pip
RUN apt-get clean


# Build frontend
FROM node:current-buster-slim as frontend
ADD lecture2gether-vue /app/src/frontend
WORKDIR /app/src/frontend
RUN rm -rf node_modules
RUN npm ci
RUN npm run build


# Combine final image
FROM backend as final
COPY --from=frontend /app/src/frontend/dist/ /app/static
# Setup configs
VOLUME /app/config
ADD docker/supervisor.conf /etc/supervisor/conf.d/app.conf
ADD docker/settings.js /app/config/settings.js
RUN ln -sf /app/config/settings.js /app/static/settings.js
ADD docker/nginx.conf /etc/nginx/sites-enabled/default

# http
EXPOSE 8000/tcp
    
CMD supervisord -n -c /etc/supervisor/supervisord.conf -u root
