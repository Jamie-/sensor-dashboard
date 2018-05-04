#!/usr/bin/env bash

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "$0: Starting Gunicorn..."
"$dir"/venv/bin/gunicorn \
    --bind 0.0.0.0:8080 \
    --log-level INFO \
    iot:app
