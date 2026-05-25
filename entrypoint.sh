#!/bin/bash
set -e

python3 manage.py migrate --no-input
python3 manage.py createsuperuser --no-input || true
python3 manage.py runserver 0.0.0.0:8000
