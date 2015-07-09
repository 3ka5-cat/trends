# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import pgettext_lazy as _


class AppConfig(AppConfig):
    name = 'core'
    verbose_name = _('Core', 'Application verbose name')

    def ready(self):
        pass