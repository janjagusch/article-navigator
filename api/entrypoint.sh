#!/bin/bash

set -eo pipefail

host="0.0.0.0"
port="8080"
workers="1"
timeout="60"
accesslog="-"

if [ -z "${GUNICORN_CMD_ARGS}" ]
then
    /usr/local/bin/gunicorn --bind "${host}":"${port}" --workers="${workers}" --timeout="${timeout}" --access-logfile "${accesslog}" app:application
else
    /usr/local/bin/gunicorn ${GUNICORN_CMD_ARGS} app:application
fi
