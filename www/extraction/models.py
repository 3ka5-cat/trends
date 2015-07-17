# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models, transaction
from django.utils.translation import pgettext_lazy
from core.models import Vacancy


class TermQuerySet(models.QuerySet):
    """ Custom queryset for filtering blacklisted terms. """
    def blacklisted(self):
        return self.filter(blacklisted=True)


class TermManager(models.Manager):
    """ Custom manager for accessing blacklisted terms and creation terms with linked vacancies. """
    def get_queryset(self):
        return TermQuerySet(self.model, using=self._db)

    def blacklisted(self):
        return self.get_queryset().blacklisted()

    def create_or_update_with_vacancies(self, name, language, vacancies_qs):
        name = name[:255]
        TermVacancyThroughModel = Term.vacancies.through
        with transaction.atomic():
            term, created = self.get_or_create(name=name, language=language)
            TermVacancyThroughModel.objects.bulk_create(map(
                lambda vacancy_id: TermVacancyThroughModel(term_id=term.id, vacancy_id=vacancy_id),
                vacancies_qs.values_list('id', flat=True)
            ))
            return term, created


class Term(models.Model):
    name = models.CharField(verbose_name=pgettext_lazy('Term field', 'Name'),
                            max_length=255, unique=True)
    language = models.CharField(verbose_name=pgettext_lazy('Term field', 'Language code (ISO 639-1)'),
                                max_length=2)
    vacancies = models.ManyToManyField(Vacancy, blank=True, null=True, related_name='terms',
                                       verbose_name=pgettext_lazy('Term field', 'Vacancies'))
    blacklisted = models.BooleanField(default=False, verbose_name=pgettext_lazy('Term field', 'Is blacklisted'))
    objects = TermManager()

    class Meta:
        verbose_name = pgettext_lazy('Term verbose name', 'Term')
        verbose_name_plural = pgettext_lazy('Term verbose plural name', 'Terms')

    def __unicode__(self):
        return self.name