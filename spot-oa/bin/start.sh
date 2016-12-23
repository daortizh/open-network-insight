#!/bin/sh
# Run ipython web server as a background service
echo -n "Starting web server... "
ipython notebook --no-mathjax --profile=ia --port=8889 --ip=0.0.0.0 --no-browser '--NotebookApp.extra_static_paths=["ui/ipython/"]'> ipython.out 2>&1&
echo "Done"
