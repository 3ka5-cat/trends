# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
import pprint
from celery import Task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.core.mail import send_mail
from django.utils.html import strip_tags
import langid
from celery_conf import app as celery_app
from core.models import Vacancy, Skill, SearchQuery
from extraction.filters import BlackListFilter
from extraction.extractors import RussianTermExtractor, EnglishTermExtractor
from extraction.models import Term
from . import api

logger = get_task_logger(__name__)


class CollectingTask(Task):
    source = 'hh.ru'
    new_vacancies = []
    unique_skills = {}
    unique_terms = {}

    search_queries = []
    existed_vacancies = 0
    existed_skills = 0
    created_skills = 0
    existed_terms = 0
    created_terms = 0
    blacklisted_terms = 0

    def run(self, *args, **kwargs):
        langid.set_languages(['ru', 'en'])
        for query in SearchQuery.objects.all():
            self.collect_data(query)
            # extract additional data
            self.extract_data()
            # save collected data
            self.store_data()
            self.search_queries.append(query.text)
        # build report
        return self.report()

    def collect_data(self, search_query):
        client = api.Client()
        requested_items = page = 0
        per_page = api.MAXIMUM_PER_PAGE
        pages_remaining = True  # for the first time, `do..while` where are you?
        while requested_items < api.MAXIMUM_RECIEVED_ITEMS and pages_remaining:
            logger.debug('Collecting page {}'.format(page))
            search_results = client.search_vacancies(text=search_query.text, area=2, specialization=1,
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

    def filter_data(self, vacancy_ids):
        # filter only not existing ids
        existing_vacancies = Vacancy.objects.filter(source=self.source,
                                                    external_id__in=vacancy_ids).values_list('external_id', flat=True)
        return [vacancy_id for vacancy_id in vacancy_ids if vacancy_id not in existing_vacancies]

    def transform_data(self, vacancy):
        # store interesting data for each vacancy
        self.new_vacancies.append({
            'external_id': vacancy['id'],
            'name': vacancy['name'],
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
        extractors = {'ru': RussianTermExtractor(filter=BlackListFilter()),
                      'en': EnglishTermExtractor(filter=BlackListFilter())}
        for vacancy in self.new_vacancies:
            language = langid.classify(vacancy['description'])[0]
            extractor = extractors[language] if language in extractors.keys() else extractors['ru']
            for item in extractor(vacancy['description']):
                term = item.normalized if isinstance(extractor, RussianTermExtractor) else item[0]
                # TODO: may be use smth like elastic search for filtering?
                if term not in self.unique_terms.keys():
                    self.unique_terms[term] = set()
                self.unique_terms[term].add(vacancy['external_id'])

    def store_data(self):
        # save batch of new vacancies, skills and terms
        with transaction.atomic():
            self.existed_vacancies = Vacancy.objects.count()
            self.existed_skills = Skill.objects.count()
            self.existed_terms = Term.objects.count()
            self.blacklisted_terms = Term.objects.blacklisted().count()
            Vacancy.objects.bulk_create(map(lambda vacancy: Vacancy(source=self.source,
                                                                    name=vacancy['name'],
                                                                    external_id=vacancy['external_id'],
                                                                    description=vacancy['description']),
                                            self.new_vacancies))

            for skill, vacancies in self.unique_skills.items():
                vacancies_qs = Vacancy.objects.filter(source=self.source, external_id__in=vacancies)
                _, created = Skill.objects.create_or_update_with_vacancies(name=skill, vacancies_qs=vacancies_qs)
                if created:
                    self.created_skills += 1

            for term, vacancies in self.unique_terms.items():
                vacancies_qs = Vacancy.objects.filter(source=self.source, external_id__in=vacancies)
                _, created = Term.objects.create_or_update_with_vacancies(name=term, language=langid.classify(term)[0],
                                                                          vacancies_qs=vacancies_qs)
                if created:
                    self.created_terms += 1

    def report(self):
        report = {
            'source': self.source,
            'search_queries': self.search_queries,
            'vacancies_existed': self.existed_vacancies,
            'vacancies_created': len(self.new_vacancies),
            'skills_created': self.created_skills,
            'skills_existed': self.existed_skills,
            'terms_created': self.created_terms,
            'terms_existed': self.existed_terms,
            'terms_blacklisted': self.blacklisted_terms,
        }
        send_mail('Collecting report', pprint.pformat(report, indent=4), 'report@trends.com',
                  ['antik.fnt@gmail.com'], fail_silently=False)
        return report


collect = celery_app.tasks[CollectingTask.name]