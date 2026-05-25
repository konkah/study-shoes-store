#!/bin/bash
set -e

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py createsuperuser --no-input || true
gunicorn study_shoes_store.wsgi:application --bind 0.0.0.0:8000
