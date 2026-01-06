#!/bin/bash
# Railway Robust Startup Script

# 1. Print current directory and files for debugging
echo "--- Current Directory Content ---"
ls -F
echo "---------------------------------"

# 2. Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# 3. Run migrations and collectstatic (optional: wrap in if for speed)
echo "[INFO] Running database migrations..."
python manage.py migrate --noinput

echo "[INFO] Collecting static files..."
python manage.py collectstatic --noinput

# 4. Starting Gunicorn
echo "[INFO] Starting Gunicorn server..."
# We use the full path to the wsgi app
gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-file - --workers 2
