#!/bin/sh

# Does user wants to listen on a particular port?
PORT="$1"

if [ "$PORT" = "" ]; then
    # Use default port
    PORT="8889"
fi

# Run web server as a background service
echo "Starting web server on port $PORT... "
BASEDIR=$(dirname $(dirname "$0"))

JUPYTER_CONFIG_DIR=./jupyter/ jupyter notebook --port=$PORT > jupyter.log 2>&1 &
