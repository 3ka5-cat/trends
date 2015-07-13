# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class AppConfig(AppConfig):
    name = 'extraction'
    verbose_name = pgettext_lazy('Application verbose name', 'Extraction')

    def ready(self):
        pass