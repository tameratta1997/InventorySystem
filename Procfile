web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --pythonpath . backend.wsgi:application --log-file - --bind 0.0.0.0:${PORT:-8000}
