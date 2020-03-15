#!/bin/bash

SRC_PATH="$(readlink "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")"
RUN_PATH=${SRC_PATH%/*}
cd "$RUN_PATH" || exit

set -xe

IMAGE_NAME=$(basename "$PWD")
IMAGE_VERSION=$(< version)

docker build \
    -t "hyoseo/""${IMAGE_NAME}":"${IMAGE_VERSION}" \
    --no-cache .