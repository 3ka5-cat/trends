# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from core.models import SearchQuery
from ..tasks import CollectingTask


@pytest.fixture
def search_query():
    text = 'python'
    SearchQuery.objects.create(text=text)
    return {'text': text}


@pytest.mark.django_db
def test_collecting_task(search_query):
    result = CollectingTask().run()