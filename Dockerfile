FROM debian:buster AS base

# Install normal dependencies
RUN apt-get update
RUN apt-get -y --no-install-recommends install python3 python3-pip python3-setuptools python3-openssl netbase nginx redis-server supervisor

# Clean apt
RUN apt-get -y autoremove
RUN apt-get clean

# Add project code to container
ADD lecture2gether_flask /app/src/backend

# Setup backend
RUN pip3 install wheel
RUN pip3 install poetry
WORKDIR /app/src/backend
RUN poetry export -nf requirements.txt | grep -v "Warning:" > requirements.txt
RUN pip3 install -r requirements.txt

FROM node:current-buster-slim as frontend

# Build frontend
ADD lecture2gether-vue /app/src/frontend
WORKDIR /app/src/frontend
RUN rm -rf node_modules
RUN rm -rf package-lock.json
RUN npm install
RUN npm run build


# Combine final image
FROM base as final
COPY --from=frontend /app/src/frontend/dist/ /app/static
# Setup configs
#ADD docker/uwsgi.ini /etc/uwsgi/lecture2gether.ini
ADD docker/supervisor.conf /etc/supervisor/conf.d/app.conf
RUN mkdir /app/config
ADD docker/settings.json /app/config/settings.json
RUN ln -sf /app/config/settings.json /app/static/settings.json
ADD docker/nginx.conf /etc/nginx/sites-enabled/default

EXPOSE 8000/tcp     # http
    
CMD supervisord -n -c /etc/supervisor/supervisord.conf -u root
