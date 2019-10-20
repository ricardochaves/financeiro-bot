#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata admin.json
python manage.py seeddb
# python manage.py collectstatic --noinput

gunicorn -w 2 -b 0.0.0.0:5005 base_site.wsgi --log-level=debug

#honcho start
