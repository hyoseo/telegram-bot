#!/bin/bash

if [ $# -eq 0 ];then
  echo you must input telegram bot token at least
elif [ $# -eq 1 ];then
  export TOKEN=$1
elif [ $# -eq 2 ];then
  export TOKEN=$1
  export WEB_PORT=$2
elif [ $# -eq 3 ];then
  export TOKEN=$1
  export WEB_PORT=$2
  export LOG_LEVEL=$3
fi

python main.py