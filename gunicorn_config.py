import os

############
###### http://docs.gunicorn.org/en/stable/settings.html#worker-processes

workers = int(os.getenv("GUNICORN_WORKS", "2"))
worker_class = "gevent"
worker_connections = int(os.getenv("GUNICORN_WORKER_CONNECTIONS", "1000"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))
keepalive = int(os.getenv("GUNICORN_KEEP_ALIVE", "2"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUEST", "200"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUEST_JITTER", "50"))

############
###### http://docs.gunicorn.org/en/stable/settings.html#logging

errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
accesslog = "-"
access_log_format = '{"message": "%(r)s", "request_id": "%({HTTP_X_REQUEST_ID}o)s", "http_status": %(s)s, "ip_address": "%(h)s", "response_length": "%(b)s", "referer": "%(f)s", "user_agent": "%(a)s", "request_time": %(L)s, "date": "%(t)s"}'
