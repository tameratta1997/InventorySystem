web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn backend.wsgi --log-file - --bind 0.0.0.0:${PORT:-8000}
