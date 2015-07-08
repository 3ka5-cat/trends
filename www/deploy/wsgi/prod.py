import os
import sys

sys.stdout = sys.stderr

# Set environmental variable for Django and fire WSGI handler
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_CONF'] = 'conf.prod'
os.environ["CELERY_LOADER"] = "django"
from django.core.wsgi import get_wsgi_application

_application = get_wsgi_application()


def application(environ, start_response):
    # Check for custom header from load balancer, and use it
    # to manually set the url_scheme variable
    environ['wsgi.url_scheme'] = environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)
