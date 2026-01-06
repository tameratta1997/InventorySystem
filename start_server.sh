#!/bin/bash
# Railway/Cloud Start Script (Flat Layout)

echo "[INFO] Running Migrations..."
python manage.py migrate --noinput

echo "[INFO] Collecting Static Files..."
python manage.py collectstatic --noinput

echo "[INFO] Starting Gunicorn..."
gunicorn backend.wsgi --log-file - --bind 0.0.0.0:${PORT:-8000}
