#!/bin/bash 

export $(egrep -v '^#' .env | xargs)

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata admin.json
# python manage.py collectstatic --noinput

#gunicorn -w $GUNICORN_WORKS -b 0.0.0.0:$PORT base_site.wsgi --log-level=debug

honcho start
