#!/bin/sh
# Stop and start web server
BASEDIR=$(dirname "$0")
$BASEDIR/stop.sh && $BASEDIR/start.sh
