#!/bin/bash
set -e

# set your environment variable to overwrite this
CONTAINER_RUNTIME=${CONTAINER_RUNTIME:-docker}

D=$(realpath $(dirname $0))
mkdir -p $D/lecture2gether_flask/.venvs

$CONTAINER_RUNTIME build -t lecture2gether --target dev $D
$CONTAINER_RUNTIME run \
    -v $D/lecture2gether-vue:/app/src/frontend \
    -v $D/lecture2gether_flask:/app/src/backend \
    -v $D/lecture2gether_flask/.venvs/:/root/.cache/pypoetry/virtualenvs \
    -p 5000:5000 \
    -p 8080:8080 \
    $@ -it --rm \
    lecture2gether

