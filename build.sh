# !/usr/bin/env bash
# exit on error
set -o errexit


poetry install --no-root 

python manage.py collectstatic  --noinput
python manage.py makemigrations
python manage.py migrate

