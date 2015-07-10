# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests

MAXIMUM_PER_PAGE = 500
MAXIMUM_RECIEVED_ITEMS = 2000


class Error(Exception):
    """ Base error for api calls. """

    def __init__(self, error, reason):
        self.error = error
        self.reason = reason

    def __str__(self):
        return 'Error({}, {})'.format(self.error, self.reason)


class Client(object):
    """ Responsable for requests to hh.ru RESTful API. """

    def __init__(self, host=None):
        self.host = 'https://api.hh.ru' if host is None else host

    def _path(self, method, *args):
        """ Creates url for calling method of hh.ru RESTful API. """
        return "{host}/{method}/{params}".format(host=self.host, method=method,
                                                 params='/'.join(args))

    def search_vacancies(self, text='', area=None, specialization=None, page=0, per_page=None):
        """ Send search on vacancies request to hh.ru RESTful API. """
        search_params = {
            'text': text,
            'area': area,
            'specialization': specialization,
            'page': page,
            'per_page': per_page
        }
        path = self._path('vacancies')
        response = requests.get(path, params=search_params)
        return response.json()

    def get_vacancy(self, id):
        """ Returns vacancy from hh.ru via RESTful API. """
        path = self._path('vacancies', id)
        response = requests.get(path)
        return response.json()