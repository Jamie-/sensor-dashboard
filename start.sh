#!/usr/bin/env bash

echo "$0: Starting IoT Logging service..."
./venv/bin/gunicorn \
    --bind 0.0.0.0:8080 \
    --log-level INFO \
    iot:app
