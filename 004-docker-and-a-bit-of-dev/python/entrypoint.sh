#!/bin/sh
set -ex

exec .venv/bin/python /app/server.py "$@"
