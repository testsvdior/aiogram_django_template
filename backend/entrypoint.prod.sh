#!/bin/sh

echo "Start prod entrypoint"
echo "Start migrate"
python manage.py migrate
echo "*************************Collect static***************************"
python manage.py collectstatic --noinput
echo "*************************Collect static***************************"
gunicorn core.wsgi:application --bind 0.0.0.0:8000