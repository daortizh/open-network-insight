#!/bin/sh

# Stop and start web server
BASEDIR=$(dirname "$0")
$BASEDIR/stop.sh $1 && $BASEDIR/start.sh $1
