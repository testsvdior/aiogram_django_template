#!/bin/sh

echo "Start prod entrypoint"
echo "Start migrate"
python manage.py migrate
echo "create superuser"
DJANGO_SUPERUSER_PASSWORD=$ADMIN_PASSWORD python manage.py createsuperuser --noinput --username $ADMIN_USERNAME --email $ADMIN_EMAIL
echo "*************************Collect static***************************"
python manage.py collectstatic --noinput
echo "*************************Collect static***************************"
gunicorn core.wsgi:application --bind 0.0.0.0:8000