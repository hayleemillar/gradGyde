#!/bin/bash

set -euo pipefail

uwsgi --ini wsgi.ini &
PID=$!
sleep 5
test -S /run/wsgi/wsgi.sock
kill -TERM $PID
wait $PID