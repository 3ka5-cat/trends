# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from celery import Task
from django.db import transaction
from core.models import Vacancy, Skill
from . import api


class CollectingTask(Task):
    source = 'hh.ru'
    new_vacancies = []
    unique_skills = {}

    def run(self, source, *args, **kwargs):
        self.source = source
        self.collect_data()

    def collect_data(self):
        client = api.Client()
        requested_items = page = 0
        per_page = api.MAXIMUM_PER_PAGE
        pages_remaining = True  # for the first time, `do..while` where are you?
        while requested_items < api.MAXIMUM_RECIEVED_ITEMS and pages_remaining:
            search_results = client.search_vacancies(text='Python', area=2, specialization=1,
                                                     page=page, per_page=per_page)
            requested_items = search_results['per_page'] * (search_results['page'] + 1)
            pages_remaining = search_results['found'] - requested_items
            # can safely increment, because of while condition
            page += 1

            vacancy_ids = map(lambda item: item['id'], search_results['items'])
            new_vacancy_ids = self.filter_data(vacancy_ids)

            # create batch of new vacancies with listed skills for each vacancy
            for new_vacancy_id in new_vacancy_ids:
                new_vacancy = client.get_vacancy(new_vacancy_id)
                self.transform_data(new_vacancy)

        # save collected data
        self.store_data()

    def filter_data(self, vacancy_ids):
        # filter only not existing ids
        existing_vacancies = Vacancy.objects.filter(source=self.source, external_id__in=vacancy_ids)
        return [vacancy_id for vacancy_id in vacancy_ids if vacancy_id not in existing_vacancies]

    def transform_data(self, vacancy):
        # store interesting data for each vacancy
        self.new_vacancies.append({
            'external_id': vacancy['id'],
            'description': vacancy['description'],
            })
        # collect data about related vacancies for each skill
        for skill in vacancy['key_skills']:
            skill_name = skill['name']
            if skill_name not in self.unique_skills.keys():
                self.unique_skills[skill_name] = []
            self.unique_skills[skill_name].append(vacancy['id'])

    def store_data(self):
        # save batch of new vacancies and update counters of skills mentioned in this vacancies
        with transaction.atomic():
            Vacancy.objects.bulk_create(map(lambda vacancy: Vacancy(source=self.source,
                                                                    external_id=vacancy['external_id'],
                                                                    description=vacancy['description']),
                                            self.new_vacancies))

            ThroughModel = Vacancy.skills.through
            for skill, vacancies in self.unique_skills.items():
                skill, created = Skill.objects.get_or_create(name=skill)
                skill.hits += len(vacancies)
                skill.save()
                ThroughModel.objects.bulk_create(map(lambda vacancy: ThroughModel(skill_id=skill.id,
                                                                                  vacancy_id=vacancy.id),
                                                     Vacancy.objects.filter(source=self.source,
                                                                            external_id__in=vacancies)))


