# encoding: utf-8

from __future__ import unicode_literals

from conf.default import *

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': 5432,
    },
}

LOGGING = create_logging_dict('/logs')

ALLOWED_HOSTS = ['hh-trends.herokuapp.com', 'www.hh-trends.herokuapp.com', ]

# Create a new project on Sentry to get the DSN value to put here.
RAVEN_CONFIG['dsn'] = ''

# use in-process cache by default
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

DEBUG = True
