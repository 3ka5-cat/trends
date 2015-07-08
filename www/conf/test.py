from conf.default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

LOGGING = create_logging_dict(location('../logs/test'))

ALLOWED_HOSTS = []

# Create a new project on Sentry to get the DSN value to put here.
RAVEN_CONFIG['dsn'] = ''
