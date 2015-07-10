# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.conf import settings

app = Celery('trends')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_envvar('DJANGO_CONF', 'conf.local')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)