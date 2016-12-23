#!/bin/sh
# Run ipython web server as a background service
echo -n "Starting web server... "
PORT="$1"

if [ "$PORT" = "" ]; then
    PORT="8889"
fi

ipython notebook --no-mathjax --profile=ia --port=$PORT --ip=0.0.0.0 --no-browser '--NotebookApp.extra_static_paths=["ui/ipython/"]'> ipython.out 2>&1&
echo "Done"
