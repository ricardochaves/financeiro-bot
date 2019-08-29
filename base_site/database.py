import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

S_DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_DATA_BASE"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "TEST": {"NAME": "mytestdatabase"},
    }
}

S_DEBUG = os.getenv("DEBUG", True)

S_SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

S_TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

S_ALLOWED_HOSTS = ["*"]

sentry_sdk.init(dsn=os.getenv("SENTRY_DNS"), integrations=[DjangoIntegration()])


S_SECRET_KEY = "3ot&@+6-ue!i)jbx-adyr-+^a(ik)$*y^tb$(98f2$1k*=$7zi"

S_LOGGING_FILE = "./logs"
