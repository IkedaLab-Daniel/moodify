#!/usr/bin/env bash

# Run migrations
python manage.py migrate --no-input

# Start Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
