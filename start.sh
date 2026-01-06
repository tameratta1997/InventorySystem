#!/bin/bash
# Railway Final Deployment Script
echo "--- Environment Check ---"
pwd
ls -F
export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH set to: $PYTHONPATH"
echo "--------------------------"

# Database operations
echo "[1/3] Running migrations..."
python manage.py migrate --noinput

echo "[2/3] Collecting static..."
python manage.py collectstatic --noinput

# Start server
echo "[3/3] Starting Gunicorn..."
gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8080} --log-file - --workers 2
