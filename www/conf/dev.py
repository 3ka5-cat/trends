# encoding: utf-8

from __future__ import unicode_literals
import dj_database_url
from conf.default import *

SECRET_KEY = get_env_variable('TRENDS_DEV_SECRET_KEY')

DATABASES = {'default': dj_database_url.config()}

LOGGING = create_logging_dict('../logs')

ALLOWED_HOSTS = ['hh-trends.herokuapp.com', 'www.hh-trends.herokuapp.com', ]

# Create a new project on Sentry to get the DSN value to put here.
RAVEN_CONFIG['dsn'] = get_env_variable('TRENDS_DEV_RAVEN_DSN')

MANDRILL_API_KEY = get_env_variable('TRENDS_DEV_MANDRILL_API_KEY')

DEBUG = True

BROKER_URL = get_env_variable('CLOUDAMQP_URL')