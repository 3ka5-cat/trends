# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import pgettext_lazy as _


class Skill(models.Model):
    name = models.CharField(verbose_name=_('Name', 'Skill field'),
                            max_length=255, unique=True)
    hits = models.IntegerField(verbose_name=_('Hits', 'Skill field'),
                               default=0)

    class Meta:
        verbose_name = _('Skill', 'Skill verbose name')
        verbose_name_plural = _('Skills', 'Skill verbose plural name')

    def __unicode__(self):
        return self.name