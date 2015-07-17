# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models, transaction
from django.utils.translation import pgettext_lazy


class Vacancy(models.Model):
    source = models.CharField(verbose_name=pgettext_lazy('Vacancy field', 'Source'),
                              max_length=255)
    external_id = models.CharField(verbose_name=pgettext_lazy('Vacancy field', 'ID in source system'),
                                   max_length=255)
    description = models.TextField(verbose_name=pgettext_lazy('Vacancy field', 'Description'),
                                   blank=True)

    class Meta:
        verbose_name = pgettext_lazy('Vacancy verbose name', 'Vacancy')
        verbose_name_plural = pgettext_lazy('Vacancy verbose plural name', 'Vacancies')
        unique_together = ('source', 'external_id')

    def __unicode__(self):
        return '{0}-{1}'.format(self.source, self.external_id)


class SkillManager(models.Manager):
    """ Custom manager for creation skill with linked vacancies. """
    def create_or_update_with_vacancies(self, name, vacancies_qs):
        SkillVacancyThroughModel = Skill.vacancies.through
        with transaction.atomic():
            skill, created = self.get_or_create(name=name)
            SkillVacancyThroughModel.objects.bulk_create(map(
                lambda vacancy_id: SkillVacancyThroughModel(skill_id=skill.id, vacancy_id=vacancy_id),
                vacancies_qs.values_list('id', flat=True)
            ))
            return skill, created


class Skill(models.Model):
    name = models.CharField(verbose_name=pgettext_lazy('Skill field', 'Name'),
                            max_length=255, unique=True)
    vacancies = models.ManyToManyField(Vacancy, blank=True, null=True, related_name='skills',
                                       verbose_name=pgettext_lazy('Skill field', 'Vacancies'))
    objects = SkillManager()

    class Meta:
        verbose_name = pgettext_lazy('Skill verbose name', 'Skill')
        verbose_name_plural = pgettext_lazy('Skill verbose plural name', 'Skills')

    def __unicode__(self):
        return self.name
