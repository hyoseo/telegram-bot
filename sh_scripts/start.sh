#!/bin/bash

SRC_PATH="$(readlink "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")"
RUN_PATH=${SRC_PATH%/*}/..
cd "$RUN_PATH" || exit

case $# in
  0)
    echo "you must input telegram bot token at least"
    ;;
  1)
    export TOKEN=$1
    nohup ./venv/bin/python3 main.py 1> /dev/null 2>&1 &
    ;;
  2)
    export TOKEN=$1
    export WEB_PORT=$2
    nohup ./venv/bin/python3 main.py 1> /dev/null 2>&1 &
    ;;
  *)
    export TOKEN=$1
    export WEB_PORT=$2
    export LOG_LEVEL=$3
    nohup ./venv/bin/python3 main.py 1> /dev/null 2>&1 &
    ;;
esac


