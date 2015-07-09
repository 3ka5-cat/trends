# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class AppConfig(AppConfig):
    name = 'hh'
    verbose_name = pgettext_lazy('Application verbose name', 'hh.ru')

    def ready(self):
        pass