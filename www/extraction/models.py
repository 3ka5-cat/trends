# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import pgettext_lazy
from core.models import Vacancy


class Term(models.Model):
    name = models.CharField(verbose_name=pgettext_lazy('Term field', 'Name'),
                            max_length=255, unique=True)
    language = models.CharField(verbose_name=pgettext_lazy('Term field', 'Language code (ISO 639-1)'),
                                max_length=2)
    vacancies = models.ManyToManyField(Vacancy, blank=True, null=True,
                                       verbose_name=pgettext_lazy('Term field', 'Vacancies'))

    class Meta:
        verbose_name = pgettext_lazy('Term verbose name', 'Term')
        verbose_name_plural = pgettext_lazy('Term verbose plural name', 'Terms')

    def __unicode__(self):
        return self.name