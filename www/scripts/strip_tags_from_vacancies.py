# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.html import strip_tags
from core.models import Vacancy


def run():
    """ Script, which strips html tags from description field for all existing vacancies. """
    vacancies = Vacancy.objects.all()
    for vacancy in vacancies.iterator():
        vacancy.description = strip_tags(vacancy.description)
        vacancy.save()