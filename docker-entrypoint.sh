#!/bin/bash

PORT=$1
sleep 2
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn water_graph.wsgi:application --workers 3 --bind 0.0.0.0:$PORT