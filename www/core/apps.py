# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class AppConfig(AppConfig):
    name = 'core'
    verbose_name = pgettext_lazy('Application verbose name', 'Core')

    def ready(self):
        pass