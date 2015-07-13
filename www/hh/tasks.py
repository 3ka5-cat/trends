# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from celery import Task
from django.db import transaction
from django.utils.html import strip_tags
import langid
from topia.termextract.extract import TermExtractor as EnglishTermExtractor
from rutermextract import TermExtractor as RussianTermExtractor
from celery_conf import app as celery_app
from core.models import Vacancy, Skill
from extraction.models import Term
from . import api


class CollectingTask(Task):
    source = 'hh.ru'
    new_vacancies = []
    unique_skills = {}
    unique_terms = {}

    def run(self, *args, **kwargs):
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

        # extract additional data
        self.extract_data()

        # save collected data
        self.store_data()

    def filter_data(self, vacancy_ids):
        # filter only not existing ids
        existing_vacancies = Vacancy.objects.filter(source=self.source,
                                                    external_id__in=vacancy_ids).values_list('external_id', flat=True)
        return [vacancy_id for vacancy_id in vacancy_ids if vacancy_id not in existing_vacancies]

    def transform_data(self, vacancy):
        # store interesting data for each vacancy
        self.new_vacancies.append({
            'external_id': vacancy['id'],
            'description': strip_tags(vacancy['description']),
            })
        # collect data about related vacancies for each skill
        for skill in vacancy['key_skills']:
            skill_name = skill['name']
            if skill_name not in self.unique_skills.keys():
                self.unique_skills[skill_name] = set()
            self.unique_skills[skill_name].add(vacancy['id'])

    def extract_data(self):
        # extract new interesting data from each vacancy
        extractors = {'ru': RussianTermExtractor(),
                      'en': EnglishTermExtractor()}
        for vacancy in self.new_vacancies:
            extractor = extractors[langid.classify(vacancy['description'])[0]]
            for item in extractor(vacancy['description']):
                term = item.normalized if isinstance(extractor, RussianTermExtractor) else item[0]
                if term not in self.unique_terms.keys():
                    self.unique_terms[term] = set()
                self.unique_terms[term].add(vacancy['external_id'])

    def store_data(self):
        # save batch of new vacancies, skills and terms
        with transaction.atomic():
            Vacancy.objects.bulk_create(map(lambda vacancy: Vacancy(source=self.source,
                                                                    external_id=vacancy['external_id'],
                                                                    description=vacancy['description']),
                                            self.new_vacancies))

            # TODO: how to bulk_create not existing skills and terms
            # and update constraints of existing effectively?
            ThroughModel = Vacancy.skills.through
            for skill, vacancies in self.unique_skills.items():
                skill, created = Skill.objects.get_or_create(name=skill)
                ThroughModel.objects.bulk_create(map(lambda vacancy: ThroughModel(skill_id=skill.id,
                                                                                  vacancy_id=vacancy.id),
                                                     Vacancy.objects.filter(source=self.source,
                                                                            external_id__in=vacancies)))
            ThroughModel = Term.vacancies.through
            for term, vacancies in self.unique_terms.items():
                term, created = Term.objects.get_or_create(name=term, language=langid.classify(term)[0])
                ThroughModel.objects.bulk_create(map(lambda vacancy: ThroughModel(term_id=term.id,
                                                                                  vacancy_id=vacancy.id),
                                                     Vacancy.objects.filter(source=self.source,
                                                                            external_id__in=vacancies)))


collect = celery_app.tasks[CollectingTask.name]