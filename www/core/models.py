# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import pgettext_lazy


class Skill(models.Model):
    name = models.CharField(verbose_name=pgettext_lazy('Skill field', 'Name'),
                            max_length=255, unique=True)
    hits = models.IntegerField(verbose_name=pgettext_lazy('Skill field', 'Hits'),
                               default=0)

    class Meta:
        verbose_name = pgettext_lazy('Skill verbose name', 'Skill')
        verbose_name_plural = pgettext_lazy('Skill verbose plural name', 'Skills')

    def __unicode__(self):
        return self.name


class Vacancy(models.Model):
    source = models.CharField(verbose_name=pgettext_lazy('Vacancy field', 'Source'),
                              max_length=255)
    external_id = models.CharField(verbose_name=pgettext_lazy('Vacancy field', 'ID in source system'),
                                   max_length=255)
    description = models.TextField(verbose_name=pgettext_lazy('Vacancy field', 'Description'),
                                   blank=True)
    skills = models.ManyToManyField(Skill, blank=True, null=True,
                                    verbose_name=pgettext_lazy('Vacancy field', 'Skills'))

    class Meta:
        verbose_name = pgettext_lazy('Vacancy verbose name', 'Vacancy')
        verbose_name_plural = pgettext_lazy('Vacancy verbose plural name', 'Vacancies')
        unique_together = ('source', 'external_id')

    def __unicode__(self):
        return '{0}-{1}'.format(self.source, self.external_id)