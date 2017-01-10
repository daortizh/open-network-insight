#!/bin/sh

# Does user wants to listen on a particular port?
PORT="$1"

if [ "$PORT" = "" ]; then
    # Use default port
    PORT="8889"
fi

# Run web server as a background service
echo -n "Starting web server... "
BASEDIR=$(dirname $(dirname "$0"))

#PYTHONPATH=$PYTHONPATH:$BASEDIR jupyter notebook --port=$PORT --config=$BASEDIR/jupyter/jupyter_notebook_config.py > jupyter.log 2>&1&
jupyter notebook --port=$PORT --config=$BASEDIR/jupyter/jupyter_notebook_config.py > jupyter.log 2>&1&
echo "Done"
