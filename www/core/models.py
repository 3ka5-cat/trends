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