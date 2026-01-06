#!/bin/bash
# Railway/Cloud Start Script

echo "[INFO] Running Migrations..."
python backend/manage.py migrate --noinput

echo "[INFO] Collecting Static Files..."
python backend/manage.py collectstatic --noinput

echo "[INFO] Starting Gunicorn..."
# cd into backend so it can find the 'backend' module correctly
cd backend
gunicorn backend.wsgi --log-file - --bind 0.0.0.0:${PORT:-8000}
