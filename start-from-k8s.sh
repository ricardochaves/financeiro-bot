#!/usr/bin/env bash

python manage.py migrate

if [[ ${DJANGO_BIND_ADDRESS+x} ]] && [[ ${DJANGO_BIND_PORT+x} ]];
then
    echo "OK! Using custom ADRESSS $DJANGO_BIND_ADDRESS and PORT $DJANGO_BIND_PORT"
    gunicorn -cpython:gunicorn_config -b ${DJANGO_BIND_ADDRESS}:${DJANGO_BIND_PORT} base_site.wsgi
else
    echo "Using 0.0.0.0:8000"
    gunicorn -cpython:gunicorn_config -b 0.0.0.0:8000 base_site.wsgi
fi
