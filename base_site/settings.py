"""
Django settings for base_site project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import datetime
import os
from logging import Formatter
from typing import Optional

import sentry_sdk

# SECURITY WARNING: keep the secret key used in production secret!
from base_site.setup.log import JsonFormatter
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = os.getenv("DEBUG") == "True"

DJANGO_ALLOWED_HOSTS: Optional[str] = os.getenv("ALLOWED_HOSTS")
if DJANGO_ALLOWED_HOSTS:
    ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["*"]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = [
    "base_site.mainapp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_swagger",
    "django_filters",
    "django_q",
    "import_export",
    "health_check",
    # "health_check.db",
    # "health_check.storage",
    "request_id_django_log",
    "base_site.nubank",
    "base_site.alelo",
    "base_site.brokes_note",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "request_id_django_log.middleware.RequestIdDjangoLog",
]

ROOT_URLCONF = "base_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "base_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_URL = "https://iluvatar-static.storage.googleapis.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "app/static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

GOOGLE_SPREADSHEET_ID = "1yO24GqWCwEW3uFHtqoqTvWgSsvZlQfi5QufTqPZq378"
GOOGLE_RANGE_NAME = "Fluxo Caixa!A1050:I"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

JWT_AUTH = {"JWT_ALLOW_REFRESH": True, "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=604800)}

Q_CLUSTER = {
    "name": "Schedule",
    "workers": 1,
    "timeout": 30,
    "retry": 600,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
}

LOGIN_URL = "/ricardo/login/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": "request_id_django_log.filters.RequestIDFilter"}},
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "standard",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "root": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
}

REQUEST_ID_CONFIG = {
    "REQUEST_ID_HEADER": "HTTP_X_REQUEST_ID",
    "GENERATE_REQUEST_ID_IF_NOT_FOUND": True,
    "RESPONSE_HEADER_REQUEST_ID": "HTTP_X_REQUEST_ID",
}

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


sentry_sdk.init(dsn=os.getenv("SENTRY_DNS"), integrations=[DjangoIntegration()])


NUBANK_CPF = os.getenv("NUBANK_CPF")
NUBANK_PASSWORD = os.getenv("NUBANK_PASSWORD")

ALELO_CPF = os.getenv("ALELO_CPF")
ALELO_PASSWORD = os.getenv("ALELO_PASSWORD")
