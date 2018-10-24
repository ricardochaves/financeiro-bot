web: gunicorn -w $GUNICORN_WORKS -b 0.0.0.0:$PORT base_site.wsgi --log-level=debug
bot: python manage.py startelegrambot2
schedule: python manage.py qcluster